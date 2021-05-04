from map_anal_models import MapAnalData
from map_variables import *
import os.path
import pickle
import map_analysis
from UserInputFetcher import fetch_user_integer

from UserInputFetcher import fetch_user_integer_with_limit


class BlockFileLoader:
    def __init__(self):
        self.total_block_dict, self.total_surface_dict, self.district_areas, self.set_of_fluids = None, None, None, None

    def run(self):
        if os.path.exists(f'{save_file_dir}{save_file_path}'):
            print('Do you want to run on save file? 1 or 2')
            keyOne = fetch_user_integer()
            #Should the user want to use a saved file
            if keyOne == 1:
                block_file = self.file_selector(save_file_dir)
                unpickled_block_file = pickle.load(block_file)
                self.load_from_pkl_file(unpickled_block_file)
            #If the user doesn't want to use a save file
            else:
                print('Do you want to save the old file before creating a new one? 1 or 2')
                keyTwo = fetch_user_integer()
                self.run_map_analysis_and_pickle_it(1) if keyTwo == 1 else self.run_map_analysis_and_pickle_it(2)
        else:
            self.run_map_analysis_and_pickle_it(2)

    def run_map_analysis_and_pickle_it(self, i: int):
        if i == 1:
            print("Give the old file a name! Please don't use space")
            file_name = str(input())
            os.rename(f"{save_file_dir}{save_file_path}", f"{save_file_dir}{file_name}_{save_file_path}")
        temp_map_data = map_analysis.MapAnalysis().run()
        self.unpack_data_object_map_anal_data(temp_map_data)
        self.write_to_pkl_file(self.district_areas, self.set_of_fluids, self.total_block_dict, self.total_surface_dict)

    def unpack_data_object_map_anal_data(self, map_anal_data: MapAnalData):
        self.total_block_dict = map_anal_data.block_dict
        self.total_surface_dict = map_anal_data.surface_dict
        self.district_areas = map_anal_data.areas_for_districts
        self.set_of_fluids = map_anal_data.set_of_fluid_coordinates

    def file_selector(self, dir_save_file):
        dirs = os.listdir(dir_save_file)
        pkl_files = []
        for index, file in enumerate(dirs):
            if file.endswith('.pkl'):
                pkl_files.append(file)
        if len(pkl_files) == 1:
            print(f"-r---currently using file {pkl_files}----")
            block_file = open(f'{save_file_dir}{pkl_files[0]}', 'rb')
        else:
            print('What save file do you want to use?')
            print('Use the number corresponding to file')
            for index, pkl in enumerate(pkl_files):
                print(f"{index}: {pkl}")
            stopper = fetch_user_integer_with_limit(len(pkl_files))
            print(f'{save_file_dir}{dirs[stopper]}')
            block_file = open(f'{save_file_dir}{dirs[stopper]}', 'rb')
        return block_file

    def load_from_pkl_file(self, unpickled_block_file):
        self.total_block_dict, self.total_surface_dict, self.district_areas, self.set_of_fluids = \
            unpickled_block_file['total_block_dict'], unpickled_block_file['total_surface_dict'], \
            unpickled_block_file['district_areas'], \
            unpickled_block_file['set_of_fluids']

    def write_to_pkl_file(self, district_areas, set_of_fluids, total_block_dict, total_surface_dict, file_name='f'):
        data = {}
        data['x_range'] = [BOX_X_MIN, BOX_X_MAX]
        data['z_range'] = [BOX_Z_MIN, BOX_Z_MAX]
        data['total_block_dict'] = total_block_dict
        data['total_surface_dict'] = total_surface_dict
        data['district_areas'] = district_areas
        data['set_of_fluids'] = set_of_fluids
        if file_name == 'f':
            with open(f'{save_file_dir}{save_file_path}', 'wb') as output:
                pickle.dump(data, output)
        else:
            with open(f'{save_file_dir}{file_name}_{save_file_path}', 'wb') as output:
                pickle.dump(data, output)