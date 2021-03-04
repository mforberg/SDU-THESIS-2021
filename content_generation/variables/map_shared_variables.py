from typing import List, Set
import copy
from pprint import pprint


class AreaMap:

    def __init__(self, coordinates: List[tuple], mass_coordinate: dict, height: int,
                 min_max_values: dict, area_set: Set[tuple]):
        self.list_of_coordinates = coordinates
        self.mass_coordinate = mass_coordinate
        self.height = height
        self.min_max_values = min_max_values
        self.area_set = area_set

    def __deepcopy__(self, memo):
        copy_object = AreaMap(self.list_of_coordinates, self.mass_coordinate, self.height, self.min_max_values,
                              self.area_set)
        return copy_object

    def __repr__(self):
        return f"<AreaMap: Coordinate Count: {len(self.list_of_coordinates)},\n" \
               f"Mass Coordinate: {pprint(self.mass_coordinate)}],\n" \
               f"Min Max: {pprint(self.min_max_values)}>"


class SolutionGA:

    def __init__(self, fitness, population: List[AreaMap]):
        self.fitness: float = fitness
        self.population = population

    def __deepcopy__(self, memo):
        copy_list = []
        for x in self.population:
            copy_list.append(copy.deepcopy(x, memo))
        copy_object = SolutionGA(self.fitness, copy_list)
        return copy_object

    def __repr__(self):
        return f"<SolutionGA: Solution Fitness: {self.fitness:.4f}, Population:{pprint(self.population)}>"
