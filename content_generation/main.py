import map_analysis
from k_means.k_means_clustering import KMeansClustering
from map_ga.map_main import AreasGA
from preprocessing.deforestation import Deforest
from type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing as WFC_PP
from wfc.preprocessing.connection_points import ConnectionPoints
from builder.wfc_builder import WFCBuilder as WFCB
from builder.surface_builder import SurfaceBuilder
from builder.test_builder import TestBuilder
from final_touch.final_main import PrepareMap
import minecraft_pb2_grpc
import grpc
import time
import json
from block_file_loader import BlockFileLoader
from map_variables import *
import uuid
from UserInputFetcher import fetch_user_integer


class Main:
    global_dict_of_used_coordinates = {}
    global_dict_of_types = {}

    def run(self):
        # tb = TestBuilder()
        SFB = SurfaceBuilder()
        # tb.build_flat_surface(type_of_block=STONE)
        # tb.create_big_areas()
        # tb.create_mexican_walls()

        #  Map analysis

        tester = BlockFileLoader()

        tester.run()

        total_block_dict, surface_dict, district_areas, set_of_fluids = tester.total_block_dict,\
                                                                              tester.total_surface_dict,\
                                                                              tester.district_areas,\
                                                                              tester.set_of_fluids

        # trees = [119, 120, 131, 132]
        # trees_for_persistence = {}
        # bulk_write_to_server_dict = {}
        # height_for_tree = {} # key = tree location, value = height of tree
        # for key in surface_dict.keys():
        #     if surface_dict[key[0], key[1]].block.type in trees:
        #         trees_for_persistence[(key[0], key[1])] = surface_dict[key[0], key[1]].block
        # for key in trees_for_persistence.keys():
        #     current_x, current_z = trees_for_persistence[key].position.x, trees_for_persistence[key].position.z
        #     current_y = trees_for_persistence[key].position.y
        #     height_of_neighbors = []
        #     counter = 0
        #     for x in range(current_x-3, current_x+3):
        #         if x < BOX_X_MAX and x > BOX_X_MIN:
        #             counter += 1
        #             height_of_neighbors.append(surface_dict[x, current_z].block.position.y)
        #     for z in range(current_z-3, current_z+3):
        #         if z < BOX_Z_MAX and z > BOX_Z_MIN:
        #             counter +=1
        #             height_of_neighbors.append(surface_dict[current_x, z].block.position.y)
        #     for index, height in enumerate(height_of_neighbors):
        #         if index < 1 or index >= len(height_of_neighbors)-1:
        #             continue
        #         height_of_neighbors[index] = (height_of_neighbors[index - 1] + height_of_neighbors[index + 1])/2
        #     height_of_neighbor = int(sum(height_of_neighbors)/counter)
        #     height_for_tree[(current_x, current_z)] = current_y - height_of_neighbor
        #     #print(current_x, current_z)
        #     #print(f"height: {height_of_neighbor}, current y: {current_y}, height_of_tree: {height_for_tree[(current_x, current_z)]}")
        #     for tree in height_for_tree:
        #         for height in range(height_of_neighbor, height_for_tree[tree]):
        #             bulk_write_to_server_dict[(tree[0], height, tree[1])] = trees_for_persistence[key]
        # SurfaceBuilder().bulk_write_air(bulk_write_to_server_dict)
        # x = input("Hol' up")
        # random_block = surface_dict[BOX_X_MIN, BOX_Z_MIN].block

        # tb.create_cuts(block=random_block)
        # tb.create_big_areas(block=random_block)

        #  Map GA
        result = AreasGA().run(areas=district_areas)

        #  K-means clustering
        clusters = KMeansClustering().run(first_ga_result=result, surface_dict=surface_dict)

        # SurfaceBuilder().build_clusters(clusters=clusters, surface_dict=surface_dict)
        #
        # self.rollback(surface_dict=surface_dict)


        #  Type GA
        first = time.time()
        # result[0] all tiles, result[1] only tiles associated with solution
        result = TypesGA().run(surface_dict=surface_dict, clusters=clusters,
                               global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
        print(f"TYPE GA: {time.time()-first}")
        for sol in result.population:
            print(sol.type_of_district)

        SFB.build_type_ga(surface_dict=surface_dict, type_ga_result=result)
        self.rollback(surface_dict=surface_dict)


        # WFC Start
        print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
        wfc_pp = WFC_PP()
        result = wfc_pp.create_tiles(result=result, tile_size=3, surface_dict=surface_dict)

        deforester = Deforest()
        deforester.run(clusters=result[1][1], surface_dict=surface_dict)
        SFB = SurfaceBuilder()

        SFB.build_wfc_glass_layer(surface_dict, result[0])
        connection_p = ConnectionPoints(clusters=result[1][1])
        connection_tiles = connection_p.run()
        wfc_pp.remove_neighbors(clustered_tiles=result[1][1])  # TODO: Maybe check this works

        SFB.build_wfc_poop_layer(surface_dict, result[1][0])
        # SFB.build_wfc_trash_layer(surface_dict, result[0])
        SFB.build_connection_tiles(surface_dict=surface_dict, connection_tiles=connection_tiles)
        x = input("Please hold xd")
        SFB.delete_wfc_glass_layer()
        SFB.delete_wfc_poop_layer()

        #SFB.delete_wfc_trash_layer()

        wfc_pp.normalize_height(clustered_tiles=result[1][1], surface_dict=surface_dict) # TODO: Implement + Test

        self.rollback(surface_dict=surface_dict)
        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End

        # Final touch
        prepare_map = PrepareMap(surface_dict=surface_dict, fluid_set=set_of_fluids)
        result = prepare_map.run(cluster_list=result[1][1], connection_tiles=connection_tiles)
        SFB.build_from_list_of_tuples(surface_dict=surface_dict, coordinates=result)
        input("Delete road?")
        SFB.delete_road_blocks()
        self.rollback(surface_dict=surface_dict)
        deforester.rollback()

    def rollback(self, surface_dict):
        print("Reset surface? 1 or 2")
        rollback = self.rollback_options()
        print("continued")
        if rollback == 1:
            SurfaceBuilder().rollback(surface_dict=surface_dict)

    def rollback_options(self):
        while True:
            rollback = fetch_user_integer()
            if rollback == 1:
                break
            elif rollback == 2:
                break
            else:
                print("Please input 1 or 2")
        return rollback


if __name__ == '__main__':
    Main().run()
