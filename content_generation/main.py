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

    def __init__(self):
        self.global_dict_of_used_coordinates = {}
        self.global_dict_of_types = {}
        self.SFB = SurfaceBuilder()
        self.tester = BlockFileLoader()
        self.surface_dict = {}

    def run(self):
        # self.create_test_map()

        SFB = SurfaceBuilder()

        #  Map analysis
        self.tester.run()

        total_block_dict, self.surface_dict, district_areas, set_of_fluids = self.tester.total_block_dict, \
                                                                        self.tester.total_surface_dict, \
                                                                        self.tester.district_areas, \
                                                                        self.tester.set_of_fluids

        #  Map GA
        result = AreasGA().run(areas=district_areas)

        #  K-means clustering
        print("Clustering Started")
        clusters = KMeansClustering().run(first_ga_result=result, surface_dict=self.surface_dict)

        # SurfaceBuilder().build_clusters(clusters=clusters, surface_dict=surface_dict)

        # self.rollback(surface_dict=surface_dict)

        #  Type GA
        first = time.time()
        # result[0] all tiles, result[1] only tiles associated with solution
        result = TypesGA().run(surface_dict=self.surface_dict, clusters=clusters,
                               global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
        print(f"TYPE GA: {time.time()-first}")
        for solution in result.population:
            print(solution.type_of_district)

        self.SFB.build_type_ga(surface_dict=self.surface_dict, type_ga_result=result)
        self.rollback(surface_dict=self.surface_dict)

        # WFC Start
        print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
        wfc_pp = WFC_PP()
        result = wfc_pp.create_tiles(result=result, tile_size=3, surface_dict=self.surface_dict)

        deforester = Deforest.getInstance()
        deforester.run(clusters=result[1][1], surface_dict=self.surface_dict)
        self.SFB.build_wfc_glass_layer(self.surface_dict, result[0])
        self.SFB.delete_wfc_glass_layer()

        connection_p = ConnectionPoints(clusters=result[1][1])
        connection_tiles = connection_p.run()

        wfc_pp.remove_neighbors(clustered_tiles=result[1][1])  # TODO: Maybe check this works

        self.SFB.build_wfc_poop_layer(self.surface_dict, result[1][0])
        # SFB.build_wfc_trash_layer(surface_dict, result[0])
        SFB.build_connection_tiles(surface_dict=surface_dict, connection_tiles=connection_tiles)
        x = input("Please hold")

        self.SFB.delete_wfc_poop_layer()

        # SFB.delete_wfc_trash_layer()

        wfc_pp.normalize_height(clustered_tiles=result[1][1], surface_dict=self.surface_dict)  # TODO: Implement + Test

        self.rollback(surface_dict=self.surface_dict)
        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End

        # Final touch
        prepare_map = PrepareMap(surface_dict=self.surface_dict, fluid_set=set_of_fluids)
        result = prepare_map.run(cluster_list=result[1][1], connection_tiles=connection_tiles)
        self.SFB.build_from_list_of_tuples(surface_dict=self.surface_dict, coordinates=result)
        input("Delete road?")
        self.SFB.delete_road_blocks()
        self.rollback(surface_dict=self.surface_dict)
        deforester.rollback()

    def rollback(self, surface_dict):
        print("Reset surface? 1 or 2")
        rollback = self.rollback_options()
        print("continued")
        if rollback == 1:
            SurfaceBuilder().rollback(surface_dict=surface_dict)

    def failsafe(self):
        self.SFB.rollback()
        Deforest.getInstance().rollback()

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

    def create_test_map(self):
        tb = TestBuilder()
        tb.build_flat_surface(type_of_block=STONE)
        tb.create_big_areas()
        tb.create_walls()


if __name__ == '__main__':
    try:
        Main().run()
    except:
        Main().failsafe()
    else:
        print("Rollback commence due to errors")
