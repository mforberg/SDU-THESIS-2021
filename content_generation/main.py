from typing import List

from k_means.k_means_clustering import KMeansClustering
from genetic_algorithm.map_ga.map_main import AreasGA
from wfc.preprocessing.deforestation import Deforest
from genetic_algorithm.type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing
from wfc.preprocessing.connection_points import ConnectionPoints
from builder.surface_builder import SurfaceBuilder
from builder.test_builder import TestBuilder
from builder.wfc_builder import WFCBuilder
from a_star.a_star_main import PrepareMap
import time
import pickle
import sys
import copy
from block_file_loader import BlockFileLoader
from map_variables import *
from UserInputFetcher import fetch_user_integer
from wfc_main import WaveFunctionCollapse
from wfc_models import Tile


class Main:

    def __init__(self):
        self.global_dict_of_used_coordinates = {}
        self.global_dict_of_types = {}
        self.SFB = SurfaceBuilder()
        self.WFC_builder = WFCBuilder()
        self.tester = BlockFileLoader()
        self.surface_dict = {}

    def run(self):
        # self.create_test_map()

        #  Map analysis
        self.tester.run()

        total_block_dict, self.surface_dict, district_areas, set_of_fluids = self.tester.total_block_dict, \
                                                                        self.tester.total_surface_dict, \
                                                                        self.tester.district_areas, \
                                                                        self.tester.set_of_fluids
        testing = True
        if not testing:
            #  Map GA
            solution_ga_without_types = AreasGA().run(areas=district_areas)

            #  K-means clustering
            print("Clustering Started")
            clusters = KMeansClustering().run(first_ga_result=solution_ga_without_types, surface_dict=self.surface_dict)

            # SurfaceBuilder().build_clusters(clusters=clusters, surface_dict=surface_dict)

            # self.rollback(surface_dict=self.surface_dict)

            #  Type GA
            first = time.time()

            final_solution_ga = TypesGA().run(surface_dict=self.surface_dict, clusters=clusters,
                                              global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
            print(f"TYPE GA: {time.time()-first}")
            # for solution in result.population:
            #     print(solution.type_of_district)

            self.SFB.build_type_ga(surface_dict=self.surface_dict, type_ga_result=final_solution_ga)
            self.rollback(surface_dict=self.surface_dict)

            # WFC Start
            print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
            wfc_pp = WFCPreprocessing()
            # result[0] all tiles, result[1] only tiles associated with solution
            result = wfc_pp.create_tiles(complete_solution_ga=final_solution_ga, tile_size=3,
                                         surface_dict=self.surface_dict)

            #  deforester = Deforest.getInstance()
            #  deforester.run(clusters=result[1][1], surface_dict=self.surface_dict)
            #  self.SFB.build_wfc_glass_layer(self.surface_dict, result[0])

            connection_p = ConnectionPoints(clusters=result[1][1])
            connection_tiles = connection_p.run()

            wfc_pp.remove_neighbors(clustered_tiles=result[1][1])  # TODO: Maybe check this works

            # self.SFB.build_wfc_absorubed_tiles_layer(self.surface_dict, result[1][0])
            # SFB.build_wfc_trash_layer(surface_dict, result[0])
            self.SFB.build_connection_tiles(surface_dict=self.surface_dict, connection_tiles=connection_tiles)
            x = input("Please hold xd")
            # SFB.delete_wfc_glass_layer()
            # self.SFB.delete_wfc_absorbed_tiles_layer()

            # self.SFB.delete_wfc_poop_layer()
            # SFB.delete_wfc_trash_layer()
            old_surface_dict = copy.deepcopy(self.surface_dict)
            new_and_old_dict = wfc_pp.normalize_height(clustered_tiles=result[1][1], surface_dict=self.surface_dict)
            self.SFB.spawn_blocks(new_and_old_dict['new'])
            input("Rebuild map?")
            self.SFB.spawn_blocks(new_and_old_dict['old'])
            self.surface_dict = old_surface_dict

            # May segfault without this line. 0x100 is a guess at the size of each stack frame.
            sys.setrecursionlimit(10000)
            clustered_tiles = result[1][1]
            #  TESTING!!!
            with open("test_files/clustered_test_file.pkl", "wb") as file:
                pickle.dump(clustered_tiles, file)
            with open("test_files/connection_test_tiles.pkl", "wb") as file:
                pickle.dump(connection_tiles, file)
                pickle.dump(connection_tiles, file)
        self.rollback(surface_dict=self.surface_dict)
        with open("test_files/clustered_test_file.pkl", "rb") as file:
            clustered_tiles = pickle.load(file)
        with open("test_files/connection_test_tiles.pkl", "rb") as file:
            connection_tiles = pickle.load(file)
        self.SFB.build_connection_tiles(surface_dict=self.surface_dict, connection_tiles=connection_tiles)
        wfc = WaveFunctionCollapse()
        list_of_collapsed_tiles = wfc.run(clustered_tiles=clustered_tiles, connection_tiles=connection_tiles)
        # amount_of_tiles = len(clustered_tiles)
        # list_of_collapsed_tiles = []
        # while not self.check_if_wfc_completed(amount_of_tiles=amount_of_tiles, tiles=list_of_collapsed_tiles):
        #     try:
        #         list_of_collapsed_tiles = wfc.run(clustered_tiles=clustered_tiles, connection_tiles=connection_tiles)
        #     except:
        #         print("we go agane")

        print(list_of_collapsed_tiles)
        input("rdy?")
        self.WFC_builder.build_collapsed_tiles(surface_dict=self.surface_dict,
                                               list_of_collapsed_tiles=list_of_collapsed_tiles)
        self.rollback(surface_dict=self.surface_dict)

        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End

        if not testing:
            # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # #  A* Start # # # # # # # # #
            prepare_map = PrepareMap(surface_dict=self.surface_dict, fluid_set=set_of_fluids)
            roads = prepare_map.run(cluster_list=result[1][1], connection_tiles=connection_tiles)
            self.SFB.build_from_list_of_tuples(surface_dict=self.surface_dict, coordinates=roads)
            input("Delete road?")
            self.SFB.delete_road_blocks()
            self.rollback(surface_dict=self.surface_dict)
            # # # # # # # # #   A* End  # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # #

            # deforester.rollback()

    def check_if_wfc_completed(self, amount_of_tiles: int, tiles: List[Tile]) -> bool:
        amount_of_tiles_done = 0
        for tile in tiles:
            if len(tile.states) > 0:
                amount_of_tiles_done += 1
        return amount_of_tiles == amount_of_tiles_done

    def rollback(self, surface_dict):
        print("Reset surface? 1 or 2")
        rollback = self.rollback_options()
        print("continued")
        if rollback == 1:
            SurfaceBuilder().rollback(surface_dict=surface_dict)

    def failsafe(self):
        self.SFB.rollback(self.surface_dict)
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
    Main().run()
    # try:
    #     Main().run()
    # except:
    #     print("ja")
    #     Main().failsafe()
    # else:
    #     print("Rollback commence due to errors")
