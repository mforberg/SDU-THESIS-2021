# from shared_variables import *
# from map_analysis import MapAnalysis
#
#
# def run_postprocess(solution: SolutionGA, surface_dict: dict):
#     for area in solution.population:
#         __check_for_digestible_areas(surface_dict=surface_dict, area=area, solution=solution)
#
#
# def __check_for_digestible_areas(solution: SolutionGA, area: SolutionArea, surface_dict: dict):
#     checked_nodes = set()
#     fluid_blocks_set = set()
#     for x in range(area.min_max_values['min_x'], area.min_max_values['max_x']):
#         for z in range(area.min_max_values['min_z'], area.min_max_values['max_z']):
#             if (x, z) in surface_dict and (x, z) not in checked_nodes:
#                 checked_nodes.add((x, z))
#                 if not __is_coordinate_part_of_another_area(x=x, z=z, solution=solution):
#                     found_area = MapAnalysis().find_area(surface_dict, x, z, checked_nodes, fluid_blocks_set)
#                     if __check_if_digest(min_max_values=area.min_max_values, area=found_area):
#                         __consume_area(consumer=area, consumed=found_area)
#
#
# def __consume_area(consumer: SolutionArea, consumed: SolutionArea):
#     for coordinate in consumed.list_of_coordinates:
#         consumer.list_of_coordinates.append(coordinate)
#
#
# def __check_if_digest(min_max_values: dict, area: SolutionArea) -> bool:
#     for coordinate in area.list_of_coordinates:
#         if coordinate[0] < min_max_values['min_x'] or coordinate[0] > min_max_values['max_x'] or \
#                 coordinate[1] < min_max_values['min_z'] or coordinate[1] > min_max_values['max_z']:
#             return False
#     return True
#
#
# def __is_coordinate_part_of_another_area(x: int, z: int, solution: SolutionGA) -> bool:
#     for area in solution.population:
#         if (x, z) in area.set_of_coordinates:
#             return True
#     return False
