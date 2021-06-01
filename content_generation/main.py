from typing import List

from k_means.k_means_clustering import KMeansClustering
from genetic_algorithm.map_ga.map_main import AreasGA
from wfc.preprocessing.deforestation import Deforest
from genetic_algorithm.type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing
from wfc.preprocessing.connection_points import ConnectionPoints, Tile
from builder.surface_builder import SurfaceBuilder
from builder.test_builder import TestBuilder
from builder.wfc_builder import WFCBuilder
from a_star.a_star_main import AStarMain
import pickle
import sys
import copy
from block_file_loader import BlockFileLoader
from map_variables import *
from UserInputFetcher import fetch_user_integer
from wfc_main import WaveFunctionCollapse


class Main:

    def __init__(self):
        self.global_dict_of_used_coordinates = {}
        self.global_dict_of_types = {}
        self.SFB = SurfaceBuilder()
        self.tester = BlockFileLoader()
        self.surface_dict = {}
        self.tile_size = 3
        self.WFC_builder = WFCBuilder(self.tile_size)
        self.new_and_old_map = dict
        self.old_surface_dict = dict

    def run(self):
        # self.create_test_map()

        #  Map analysis
        self.tester.run()

        total_block_dict, self.surface_dict, district_areas, set_of_fluids = self.tester.total_block_dict, \
                                                                             self.tester.total_surface_dict, \
                                                                             self.tester.district_areas, \
                                                                             self.tester.set_of_fluids
        testing = False
        if not testing:
            #  Map GA
            solution_ga_without_types = AreasGA().run(areas=district_areas)

            #  K-means clustering
            print("Clustering Started")
            clusters = KMeansClustering().run(first_ga_result=solution_ga_without_types, surface_dict=self.surface_dict)

            # SurfaceBuilder().build_clusters(clusters=clusters, surface_dict=self.surface_dict)
            # self.rollback(surface_dict=self.surface_dict)

            #  Type GA
            final_solution_ga = TypesGA().run(surface_dict=self.surface_dict, clusters=clusters,
                                              global_district_types_dict=self.global_dict_of_types,
                                              fluid_set=set_of_fluids)

            # self.SFB.build_type_ga(surface_dict=self.surface_dict, type_ga_result=final_solution_ga)
            # self.rollback(surface_dict=self.surface_dict)

            # WFC Start
            print("- - - - WFC ALGORITHM STARTING - - - -")
            wfc_pp = WFCPreprocessing(tile_size=self.tile_size)
            # result[0] all tiles, result[1] only tiles associated with solution
            result = wfc_pp.create_tiles(complete_solution_ga=final_solution_ga,
                                         surface_dict=self.surface_dict)
            clustered_tiles = result[1][1]

            deforester = Deforest.getInstance()
            deforester.run(clusters=clustered_tiles, surface_dict=self.surface_dict)

            wfc_pp.remove_neighbors(clustered_tiles=clustered_tiles)

            self.old_surface_dict = copy.deepcopy(self.surface_dict)
            self.new_and_old_map = wfc_pp.normalize_height(clustered_tiles=clustered_tiles,
                                                           surface_dict=self.surface_dict)
            self.SFB.spawn_blocks(self.new_and_old_map['new'])

            connection_p = ConnectionPoints(clusters=clustered_tiles)
            connection_tiles = connection_p.run()
            self.SFB.build_connection_tiles(surface_dict=self.surface_dict, connection_tiles=connection_tiles)

            # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # #  A* Start # # # # # # # # #
            a_star = AStarMain(surface_dict=self.surface_dict, fluid_set=set_of_fluids)
            roads = a_star.run(cluster_list=clustered_tiles, connection_tiles=connection_tiles)
            self.SFB.build_roads(surface_dict=self.surface_dict, coordinates=roads, block_type=COBBLESTONE)
            # # # # # # # # #   A* End  # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # #

            # May segfault without this line. 0x100 is a guess at the size of each stack frame.
            sys.setrecursionlimit(10000)

            #  TESTING!!!
            with open("test_files/clustered_test_file.pkl", "wb") as file:
                pickle.dump(clustered_tiles, file)
            with open("test_files/connection_test_tiles.pkl", "wb") as file:
                pickle.dump(connection_tiles, file)

        with open("test_files/clustered_test_file.pkl", "rb") as file:
            clustered_tiles = pickle.load(file)
        with open("test_files/connection_test_tiles.pkl", "rb") as file:
            connection_tiles = pickle.load(file)

        wfc = WaveFunctionCollapse(tile_size=self.tile_size)

        list_of_collapsed_tiles = wfc.run(clustered_tiles=clustered_tiles, connection_tiles=connection_tiles)

        self.WFC_builder.build_collapsed_tiles(surface_dict=self.surface_dict,
                                               list_of_collapsed_tiles=list_of_collapsed_tiles)

        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End
        if testing:
            input("Ready to delete?")
            self.WFC_builder.remove_buildings()
            SurfaceBuilder().rollback(surface_dict=self.surface_dict)
        else:
            input("Reset map...")
            print("Continued")
            self.SFB.delete_road_blocks()
            self.WFC_builder.remove_buildings()
            SurfaceBuilder().rollback(surface_dict=self.surface_dict)
            self.SFB.spawn_blocks(self.new_and_old_map['old'])
            SurfaceBuilder().rollback(surface_dict=self.old_surface_dict)
            deforester = Deforest.getInstance()
            deforester.rollback()

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
        # tb.create_big_areas(block_type=BEDROCK)
        tb.create_walls(block_type=AIR)

    def check_if_wfc_completed(self, amount_of_tiles: int, tiles: List[Tile]) -> bool:
        amount_of_tiles_done = 0
        for tile in tiles:
            if len(tile.states) > 0:
                amount_of_tiles_done += 1
        return amount_of_tiles == amount_of_tiles_done


if __name__ == '__main__':
    Main().run()
