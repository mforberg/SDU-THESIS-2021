from typing import List
import copy
from pprint import pprint
import uuid


class SolutionArea:

    def __init__(self, coordinates: List[tuple], mass_coordinate: dict, height: float, type_of_district: str,
                 min_max_values: dict):
        self.list_of_coordinates = coordinates
        self.set_of_coordinates = set(coordinates)
        self.mass_coordinate = mass_coordinate
        self.height = height
        self.min_max_values = min_max_values
        self.type_of_district = type_of_district
        self.id = str(uuid.uuid4())

    def __deepcopy__(self, memo):
        copy_object = SolutionArea(coordinates=self.list_of_coordinates, mass_coordinate=self.mass_coordinate,
                                   height=self.height, min_max_values=self.min_max_values,
                                   type_of_district=self.type_of_district)
        return copy_object

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): Coordinate Count: {len(self.list_of_coordinates)}, " \
               f"Mass Coordinate: {self.mass_coordinate}, " \
               f"Min Max: {self.min_max_values}>\n"

    def recalculate(self):
        min_x = min_z = 999999999999999999999999999999999999999999999
        max_x = max_z = -99999999999999999999999999999999999999999999
        total_x = total_z = 0
        for coordinate in self.list_of_coordinates:
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
        mass_x, mass_z = total_x / len(self.list_of_coordinates), total_z / len(self.list_of_coordinates)
        self.mass_coordinate = {"x": mass_x, "z": mass_z}
        self.min_max_values = {"min_x": min_x, "max_x": max_x, "min_z": min_z, "max_z": max_z}


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
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.fitness:.2f}, Population:\n {self.population}>"
