import map_analysis
from k_means.k_means_clustering import KMeansClustering
from map_ga.map_main import AreasGA
from type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing as WFC_PP
from builder.wfc_builder import WFCBuilder as WFCB
from builder.surface_builder import SurfaceBuilder
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
        #  Map analysis

        tester = BlockFileLoader()

        tester.run()

        total_block_dict, surface_dict, district_areas, set_of_fluids = tester.total_block_dict,\
                                                                              tester.total_surface_dict,\
                                                                              tester.district_areas,\
                                                                              tester.set_of_fluids
        #  Map GA
        result = AreasGA().run(areas=district_areas)

        #  K-means clustering
        clusters = KMeansClustering().run(first_ga_result=result, surface_dict=surface_dict)

        SurfaceBuilder().build_clusters(clusters=clusters, surface_dict=surface_dict)

        self.rollback(surface_dict=surface_dict)

        #  Type GA
        first = time.time()
        # result[0] all tiles, result[1] only tiles associated with solution
        result = TypesGA().run(surface_dict=surface_dict, clusters=clusters,
                               global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
        print(f"TYPE GA: {time.time()-first}")

        SurfaceBuilder().build_type_ga(surface_dict=surface_dict, type_ga_result=result)
        self.rollback(surface_dict=surface_dict)


        # WFC Start
        print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
        result = WFC_PP().create_tiles(result=result, tile_size=3, surface_dict=surface_dict)
        WFCB().build_tiles(surface_dict=surface_dict, tiles=result)
        SFB = SurfaceBuilder()
        #SFB.build_wfc_glass_layer(surface_dict, result)
        SFB.build_wfc_trash_layer(surface_dict, result)
        #SFB.delete_wfc_glass_layer()
        SFB.delete_wfc_trash_layer()
        self.rollback(surface_dict=surface_dict)
        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End

        # Final touch
        # prepare_map = PrepareMap(surface_dict=surface_dict, fluid_set=set_of_fluids)
        # result = prepare_map.run(blocked_coordinates={(0, 0)}, connection_points=[[(BOX_X_MIN, BOX_Z_MIN),
        #                                                                            (BOX_X_MAX, BOX_Z_MAX)]])
        # SurfaceBuilder().build_from_list_of_tuples(surface_dict=surface_dict, coordinates=result)
        # self.rollback(surface_dict=surface_dict)

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
