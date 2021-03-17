from variables.shared_variables import *
from variables.ga_type_variables import *
from minecraft_pb2 import *


def run_preprocess(solution: SolutionGA, surface_dict: dict, fluid_set: set) -> dict:
    preprocess_dict = {}
    city_center_x = 0
    city_center_z = 0
    for area in solution.population:
        amount_dict = __find_amount_of_water_stone_and_wood(area=area, fluid_set=fluid_set, surface_dict=surface_dict)
        preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])] = amount_dict
        city_center_x += area.mass_coordinate['x']
        city_center_z += area.mass_coordinate['z']
    preprocess_dict['city_center'] = {'x': city_center_x/len(solution.population),
                                      'z': city_center_z/len(solution.population)}
    return preprocess_dict


def __find_amount_of_water_stone_and_wood(area: SolutionArea, fluid_set: set, surface_dict: dict) -> PreProcessData:
    min_x = area.min_max_values['min_x']
    max_x = area.min_max_values['max_x']
    min_z = area.min_max_values['min_z']
    max_z = area.min_max_values['max_z']
    list_of_water = []
    list_of_resources = []
    outside_modifier = TYPE_AREA_AROUND_DISTRICT_TO_BE_CHECKED
    for x in range(min_x - outside_modifier, max_x + outside_modifier):
        for z in range(min_z - outside_modifier, max_z + outside_modifier):
            if (x, z) in fluid_set:
                list_of_water.append((x, z))
            else:
                if (x, z) in surface_dict:
                    block_type = surface_dict[(x, z)].block_type
                    if block_type == STONE or block_type == LOG or block_type == LOG2:
                        list_of_resources.append((x, z))
    return PreProcessData(water_list=list_of_water, resource_list=list_of_resources)
