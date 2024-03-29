import copy
import math
import uuid
from typing import List


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

    def distance_to_mass_coordinate(self, x, z) -> float:
        return math.sqrt((math.pow(x - self.mass_coordinate['x'], 2) + math.pow(z - self.mass_coordinate['z'], 2)))

    def check_if_neighbor_to_coordinate(self, x: int, z: int, surface_dict: dict) -> bool:
        y = surface_dict[(x, z)].y
        for coordinate in self.list_of_coordinates:
            amount = abs(coordinate[0] - x) + abs(coordinate[1] - z)
            if amount <= 1 and abs(surface_dict[(coordinate[0], coordinate[1])].y - y) <= 1:
                return True
        return False

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): Coordinate Count: {len(self.list_of_coordinates)}, " \
               f"Mass Coordinate: {self.mass_coordinate}, " \
               f"Min Max: {self.min_max_values}>\n"

    def recalculate_min_max_mass(self):
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

    def recalculate_height(self, surface_dict: dict):
        total_y = 0
        for coordinate in self.list_of_coordinates:
            total_y += surface_dict[coordinate].y
        self.height = total_y / len(self.list_of_coordinates)

    def __eq__(self, other):
        self_mass_coordinate = (int(self.mass_coordinate['x']), int(self.mass_coordinate['z']))
        other_mass_coordinate = (int(other.mass_coordinate['x']), int(other.mass_coordinate['z']))
        if self_mass_coordinate == other_mass_coordinate:
            return True
        return False


class SolutionGA:

    def __init__(self, fitness: float, population: List[SolutionArea]):
        self.fitness = fitness
        self.population = population

    def update_sets(self):
        for value in self.population:
            value.set_of_coordinates = set(value.list_of_coordinates)

    def __deepcopy__(self, memo):
        copy_list = []
        for x in self.population:
            copy_list.append(copy.copy(x))
        copy_object = SolutionGA(self.fitness, copy_list)
        return copy_object

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.fitness:.2f}, Population:\n {self.population}>"


class SurfaceDictionaryValue:

    def __init__(self, y: int, block_type: int, block):
        self.y = y
        self.block_type = block_type
        self.block = block


def calculate_mass_coordinate(list_of_coordinates: List[tuple]) -> tuple:
    if len(list_of_coordinates) <= 0:
        return ()
    total_x = 0
    total_z = 0
    for coordinate in list_of_coordinates:
        total_x += coordinate[0]
        total_z += coordinate[1]
    return total_x / len(list_of_coordinates), total_z / len(list_of_coordinates)