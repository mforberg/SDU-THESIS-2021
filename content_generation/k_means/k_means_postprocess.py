from variables.shared_variables import *


def recalculate_to_solution_ga(clusters: List[List[list]]) -> SolutionGA:
    solution_ga = SolutionGA(fitness=0, population=[])
    for cluster in clusters:
        solution_ga.population.append(__create_solution_area_from_cluster(cluster=cluster))
    return solution_ga


def __create_solution_area_from_cluster(cluster: List[list]) -> SolutionArea:
    new_list = []
    min_x = min_z = 999999999999999999999999999999999999999999999
    max_x = max_z = -99999999999999999999999999999999999999999999
    total_x = total_z = 0
    for coordinate in cluster:
        x, z = coordinate[0], coordinate[1]
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
    mass_x, mass_z = total_x / len(cluster), total_z / len(cluster)
    return SolutionArea(coordinates=new_list, mass_coordinate={"x": mass_x, "z": mass_z}, height=-1,
                        type_of_district="wait", min_max_values={"min_x": min_x, "max_x": max_x, "min_z": min_z,
                                                                 "max_z": max_z})
