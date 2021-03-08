import map_analysis
from k_means.k_means_clustering import KMeansClustering
from map_ga.map_main import AreasGA
from type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing as WFC_PP
from builder.wfc_builder import WFCBuilder as WFCB
import minecraft_pb2_grpc
import grpc
import time
import copy


class Main:
    global_dict_of_used_coordinates = {}
    global_dict_of_types = {}

    def run(self):
        #  Map analysis
        total_block_dict, total_surface_dict, district_areas, set_of_fluids = map_analysis.MapAnalysis().run()

        #  Map GA
        result = AreasGA().run(areas=district_areas)

        #  K-means clustering
        clusters = KMeansClustering().run(first_ga_result=result)

        WFCB().build_clusters(clusters=clusters, surface_dict=total_surface_dict)
        rollback = input("reset surface? Y/n - type anything and it will not rollback")
        print("continued")
        if not rollback:
            WFCB().rollback(surface_dict=total_surface_dict)

        #  Type GA
        first = time.time()
        result = TypesGA().run(surface_dict=total_surface_dict, clusters=clusters,
                               global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
        print(f"TYPE GA: {time.time()-first}")

        WFCB().build_type_ga(surface_dict=total_surface_dict, type_ga_result=result)
        rollback = input("reset surface? Y/n - type anything and it will not rollback")
        print("continued")
        if not rollback:
            WFCB().rollback(surface_dict=total_surface_dict)


        # WFC Start
        print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
        result = WFC_PP().create_tiles(result=result, tile_size=2)
        WFCB().build_tiles(surface_dict=total_surface_dict, tiles=result)
        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End


if __name__ == '__main__':
    Main().run()
