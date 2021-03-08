from variables.shared_variables import *
from variables.ga_type_variables import *
from minecraft_pb2 import *


def run_preprocess(solution: SolutionGA, surface_dict: dict, fluid_set: set) -> dict:
    preprocess_dict = {}
    city_center_x = 0
    city_center_z = 0
    for area in solution.population:
        water_amount = find_amount_of_water(area=area, fluid_set=fluid_set)
        preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])] = water_amount
        city_center_x += area.mass_coordinate['x']
        city_center_z += area.mass_coordinate['z']
    preprocess_dict['city_center'] = {'x': city_center_x/len(solution.population),
                                      'z': city_center_z/len(solution.population)}
    return preprocess_dict


def find_amount_of_water(area: SolutionArea, fluid_set: set) -> int:
    min_x = area.min_max_values['min_x']
    max_x = area.min_max_values['max_x']
    min_z = area.min_max_values['min_z']
    max_z = area.min_max_values['max_z']
    amount_of_water_found = 0
    outside_modifier = FITNESS_TYPE_FISHING_LENGTH_OF_AREA_AROUND_DISTRICT_TO_CHECK
    for x in range(min_x - outside_modifier, max_x + outside_modifier):
        for z in range(min_z - outside_modifier, max_z + outside_modifier):
            if (x, z) in fluid_set:
                amount_of_water_found += 1
    return amount_of_water_found
