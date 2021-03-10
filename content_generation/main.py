import map_analysis
from k_means.k_means_clustering import KMeansClustering
from map_ga.map_main import AreasGA
from type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing as WFC_PP
from builder.wfc_builder import WFCBuilder as WFCB
from builder.surface_builder import SurfaceBuilder
import minecraft_pb2_grpc
import grpc
import time
import copy
import json
import pickle
from map_variables import *
import os.path
import uuid

class Main:
    global_dict_of_used_coordinates = {}
    global_dict_of_types = {}


    def check_range(self, file):
        x_range = file['x_range']
        z_range = file['z_range']

        if x_range[0] == BOX_X_MIN and x_range[1] == BOX_X_MAX and z_range[0] == BOX_Z_MIN and z_range[1] == BOX_Z_MAX:
            return True
        else:
            return False

    def run(self):
        #  Map analysis
        total_block_dict, total_surface_dict, district_areas, set_of_fluids = None, None, None, None
        block_file = None
        print('1 means yes. 2 means no')
        if os.path.exists(f'{save_file_dir}{save_file_path}'):
            print('Do you want to run on save file? 1 or 2')
            user_input_for_test = int(input())
            if user_input_for_test == 1:
                print('What save file do you want to use?')
                print('Use the number corresponding to file')
                dirs = os.listdir(save_file_dir)
                for index, file in enumerate(dirs):
                    if file.endswith('.pkl'):
                        print(f'{index}: {file}')
                stopper = int(input())
                block_file = open(f'{save_file_dir}{dirs[stopper]}', 'rb')
                unpickled_block_file = pickle.load(block_file)
                if self.check_range(unpickled_block_file):
                    total_block_dict, total_surface_dict, district_areas, set_of_fluids =\
                        unpickled_block_file['total_block_dict'], unpickled_block_file['total_surface_dict'], unpickled_block_file['district_areas'],\
                        unpickled_block_file['set_of_fluids']
            else:
                print('Do you want to save the old file before creating a new one? 1 or 2')
                user_input_for_old_file_saving = int(input())
                if user_input_for_old_file_saving == 1:
                    print("Give the file a name! Please don't use space")
                    file_name = str(input())
                    total_block_dict, total_surface_dict, district_areas, set_of_fluids = map_analysis.MapAnalysis().run()
                    data = {}
                    data['x_range'] = [BOX_X_MIN, BOX_X_MAX]
                    data['z_range'] = [BOX_Z_MIN, BOX_Z_MAX]
                    data['total_block_dict'] = total_block_dict
                    data['total_surface_dict'] = total_surface_dict
                    data['district_areas'] = district_areas
                    data['set_of_fluids'] = set_of_fluids
                    with open(f'{save_file_dir}{file_name}_{save_file_path}', 'wb') as output:
                        pickle.dump(data, output)
                else:
                    total_block_dict, total_surface_dict, district_areas, set_of_fluids = map_analysis.MapAnalysis().run()
                    self.write_to_pkl_file(district_areas, set_of_fluids, total_block_dict, total_surface_dict)
        else:
            total_block_dict, total_surface_dict, district_areas, set_of_fluids = map_analysis.MapAnalysis().run()
            self.write_to_pkl_file(district_areas, set_of_fluids, total_block_dict, total_surface_dict)

        #  Map GA
        result = AreasGA().run(areas=district_areas)

        #  K-means clustering
        clusters = KMeansClustering().run(first_ga_result=result, surface_dict=total_surface_dict)

        SurfaceBuilder().build_clusters(clusters=clusters, surface_dict=total_surface_dict)
        print("Reset surface? 1 or 2")
        rollback = int(input())
        print("continued")
        if rollback == 1:
            SurfaceBuilder().rollback(surface_dict=total_surface_dict)
        # return

        #  Type GA
        first = time.time()
        result = TypesGA().run(surface_dict=total_surface_dict, clusters=clusters,
                               global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
        print(f"TYPE GA: {time.time()-first}")

        SurfaceBuilder().build_type_ga(surface_dict=total_surface_dict, type_ga_result=result)
        print("Reset surface? 1 or 2")
        rollback = int(input())
        print("continued")
        if rollback == 1:
            SurfaceBuilder().rollback(surface_dict=total_surface_dict)


        # WFC Start
        print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
        result = WFC_PP().create_tiles(result=result, tile_size=2)
        WFCB().build_tiles(surface_dict=total_surface_dict, tiles=result)
        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End

    def write_to_pkl_file(self, district_areas, set_of_fluids, total_block_dict, total_surface_dict):
        data = {}
        data['x_range'] = [BOX_X_MIN, BOX_X_MAX]
        data['z_range'] = [BOX_Z_MIN, BOX_Z_MAX]
        data['total_block_dict'] = total_block_dict
        data['total_surface_dict'] = total_surface_dict
        data['district_areas'] = district_areas
        data['set_of_fluids'] = set_of_fluids
        with open(f'{save_file_dir}{save_file_path}', 'wb') as output:
            pickle.dump(data, output)


if __name__ == '__main__':
    Main().run()
