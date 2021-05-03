from typing import List
import copy
import uuid
import math
import csv
from os import path


def calculate_mass_coordinate(list_of_coordinates: List[tuple]) -> tuple:
    if len(list_of_coordinates) <= 0:
        return ()
    total_x = 0
    total_z = 0
    for coordinate in list_of_coordinates:
        total_x += coordinate[0]
        total_z += coordinate[1]
    return total_x / len(list_of_coordinates), total_z / len(list_of_coordinates)


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
            copy_list.append(copy.deepcopy(x, memo))
        copy_object = SolutionGA(self.fitness, copy_list)
        return copy_object

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.fitness:.2f}, Population:\n {self.population}>"


class SurfaceDictionaryValue:

    def __init__(self, y: int, block_type: int, block):
        self.y = y
        self.block_type = block_type
        self.block = block


class DataFileCreator:

    def __init__(self, filename: str):
        self.folder = "stats/"
        i = 1
        new_file_name = filename
        while path.exists(f"{self.folder}{new_file_name}.csv"):
            new_file_name = filename + str(i)
            i += 1
        self.filename = new_file_name

    def check_stats_on_solution(self, population: List[SolutionGA], current_gen: int, best_solution: SolutionGA):
        new_best_prints = []
        min_fitness = 99999999999999
        max_fitness = -1
        avg_fitness = 0
        for solution in population:
            fitness = solution.fitness
            avg_fitness += fitness
            if fitness < min_fitness:
                min_fitness = fitness
            elif fitness > max_fitness:
                max_fitness = fitness
                if fitness > best_solution.fitness:
                    best_solution = copy.deepcopy(solution)
                    new_best_prints.append(f"New best {solution.fitness} at gen {current_gen}")
        data = {'Min': min_fitness, 'Max': max_fitness, 'Avg': avg_fitness / len(population)}
        # self.__store_stats(gen=current_gen, data=data)
        return new_best_prints, best_solution

    def __store_stats(self, gen: int, data: dict):
        with open(f"{self.folder}{self.filename}.csv", "a", newline='') as file:
            fieldnames = ['Generation', 'Min_fitness', 'Max_fitness', 'Avg_fitness']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'Generation': gen, 'Min_fitness': data['Min'], 'Max_fitness': data['Max'],
                             'Avg_fitness': data['Avg']})
