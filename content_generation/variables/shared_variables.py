from typing import List
import copy
from pprint import pprint


class SolutionArea:

    def __init__(self, coordinates: List[tuple], mass_coordinate: dict, height: int, type_of_district: str,
                 min_max_values: dict):
        self.list_of_coordinates = coordinates
        self.mass_coordinate = mass_coordinate
        self.height = height
        self.min_max_values = min_max_values
        self.type_of_district = type_of_district

    def __deepcopy__(self, memo):
        copy_object = SolutionArea(coordinates=self.list_of_coordinates, mass_coordinate=self.mass_coordinate,
                                   height=self.height, min_max_values=self.min_max_values,
                                   type_of_district=self.type_of_district)
        return copy_object

    def __repr__(self):
        return f"<AreaMap: Coordinate Count: {len(self.list_of_coordinates)},\n" \
               f"Mass Coordinate: {pprint(self.mass_coordinate)}],\n" \
               f"Min Max: {pprint(self.min_max_values)}>"


class SolutionGA:

    def __init__(self, fitness: float, population: List[SolutionArea]):
        self.fitness = fitness
        self.population = population

    def __deepcopy__(self, memo):
        copy_list = []
        for x in self.population:
            copy_list.append(copy.deepcopy(x, memo))
        copy_object = SolutionGA(self.fitness, copy_list)
        return copy_object

    def __repr__(self):
        return f"<SolutionGA: Solution Fitness: {self.fitness:.4f}, Population:{pprint(self.population)}>"
