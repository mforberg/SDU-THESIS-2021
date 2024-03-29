from models.shared_models import *
from map_analysis import MapAnalysis
from variables.map_variables import FLUID_SET


def run_postprocess(centroids: List[list], surface_dict: dict) -> SolutionGA:
    solution = __recalculate_to_solution_ga(clusters=centroids, surface_dict=surface_dict)
    solution.population.sort(key=lambda x: len(x.list_of_coordinates))
    for area in solution.population:
        __check_for_and_consume_digestible_areas(surface_dict=surface_dict, area=area, solution=solution)
        area.recalculate_min_max_mass()
        area.recalculate_height(surface_dict=surface_dict)
    return solution


def __check_for_and_consume_digestible_areas(solution: SolutionGA, area: SolutionArea, surface_dict: dict):
    checked_nodes = set()
    fluid_blocks_set = set()
    found_areas = []
    for x in range(area.min_max_values['min_x'], area.min_max_values['max_x']):
        for z in range(area.min_max_values['min_z'], area.min_max_values['max_z']):
            if (x, z) in surface_dict and (x, z) not in checked_nodes:
                checked_nodes.add((x, z))
                if not __is_coordinate_part_of_another_area(x=x, z=z, solution=solution):
                    found_areas.append(MapAnalysis().find_area(surface_dict, x, z, checked_nodes, fluid_blocks_set))
    found_areas.sort(key=lambda consumed_area: consumed_area.distance_to_mass_coordinate(x=area.mass_coordinate['x'],
                                                                                         z=area.mass_coordinate['z']))
    for found_area in found_areas:
        if __check_if_digest(consumer=area, consumed=found_area, surface_dict=surface_dict):
            if __check_if_area_is_connected_to_consumer(consumer=area, consumed=found_area, surface_dict=surface_dict):
                __consume_area(consumer=area, consumed=found_area)


def __check_if_area_is_connected_to_consumer(consumer: SolutionArea, consumed: SolutionArea,
                                             surface_dict: dict) -> bool:
    for coordinate in consumer.list_of_coordinates:
        if consumed.check_if_neighbor_to_coordinate(x=coordinate[0], z=coordinate[1], surface_dict=surface_dict):
            return True
    return False


def __consume_area(consumer: SolutionArea, consumed: SolutionArea):
    for coordinate in consumed.list_of_coordinates:
        consumer.list_of_coordinates.append(coordinate)


def __check_if_digest(consumer: SolutionArea, consumed: SolutionArea, surface_dict: dict) -> bool:
    min_max_values = consumer.min_max_values
    for coordinate in consumed.list_of_coordinates:
        type_of_block = surface_dict[coordinate].block_type
        if type_of_block in FLUID_SET:
            return False
        if coordinate[0] < min_max_values['min_x'] or coordinate[0] > min_max_values['max_x'] or \
                coordinate[1] < min_max_values['min_z'] or coordinate[1] > min_max_values['max_z'] \
                or abs(consumer.height - consumed.height) > 5:
            return False
    return True


def __is_coordinate_part_of_another_area(x: int, z: int, solution: SolutionGA) -> bool:
    for area in solution.population:
        if (x, z) in area.set_of_coordinates:
            return True
    return False


def __recalculate_to_solution_ga(clusters: List[List[list]], surface_dict: dict) -> SolutionGA:
    solution_ga = SolutionGA(fitness=0, population=[])
    for cluster in clusters:
        solution_ga.population.append(__create_solution_area_from_cluster(cluster=cluster, surface_dict=surface_dict))
    return solution_ga


def __create_solution_area_from_cluster(cluster: List[list], surface_dict: dict) -> SolutionArea:
    new_list = []
    min_x = min_z = 999999999999999999999999999999999999999999999
    max_x = max_z = -99999999999999999999999999999999999999999999
    total_x = total_z = 0
    total_y = 0
    for coordinate in cluster:
        x, z = coordinate[0], coordinate[1]
        total_y += surface_dict[(x, z)].y
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if z < min_z:
            min_z = z
        elif z > max_z:
            max_z = z
        total_x += x
        total_z += z
        new_list.append((x, z))
    mass_x, mass_z, average_y = total_x / len(cluster), total_z / len(cluster), total_y / len(cluster)
    return SolutionArea(coordinates=new_list, mass_coordinate={"x": mass_x, "z": mass_z}, height=average_y,
                        type_of_district="wait", min_max_values={"min_x": min_x, "max_x": max_x, "min_z": min_z,
                                                                 "max_z": max_z})
