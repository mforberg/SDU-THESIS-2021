import math
from variables.ga_map_variables import *
from variables.map_variables import MIN_SIZE_OF_AREA
from variables.shared_variables import *


class MapFitness:

    avg_y = 0
    mass_center = {'x': 0, 'z': 0}
    x_and_z = math.sqrt(MIN_SIZE_OF_AREA)
    min_value_for_fitness_distance = (x_and_z * x_and_z) / math.sqrt(math.pow(x_and_z, 2) + math.pow(x_and_z, 2))

    def calculate_fitness_for_all(self, population_list: List[SolutionGA]):
        for population in population_list:
            self.__calculate_individual_fitness(population)

    def __calculate_individual_fitness(self, solution: SolutionGA):
        self.avg_y = 0
        self.mass_center = {'x': 0, 'z': 0}
        solution.fitness = self.__calculate_fitness_from_population(solution.population)

    def __calculate_fitness_from_population(self, population: List[SolutionArea]) -> float:
        mass_centers = []
        height_list = []
        area_masses = []
        total_x = total_z = total_y = current_fitness = per_area_fitness = 0
        duplicate_areas = {}  # key = mass_coordinate, value = [repetitions, length]
        for area in population:
            if (area.mass_coordinate['x'], area.mass_coordinate['z']) in duplicate_areas:
                duplicate_areas[(area.mass_coordinate['x'], area.mass_coordinate['z'])]['repetitions'] += 1  # should increase repetitions with 1
            else:
                duplicate_areas[(area.mass_coordinate['x'], area.mass_coordinate['z'])] = {'repetitions': 1, 'length': len(area.list_of_coordinates)}
            per_area_fitness += self.__size_fitness(area.list_of_coordinates, area.min_max_values)
            mass_centers.append(area.mass_coordinate)
            height_list.append(area.height)
            total_x += area.mass_coordinate['x']
            total_z += area.mass_coordinate['z']
            total_y += area.height
            area_masses.append(len(area.set_of_coordinates))
        population_len = len(population)
        self.mass_center = {'x': total_x / population_len, 'z': total_z / population_len}
        self.avg_y = total_y / population_len
        current_fitness += per_area_fitness / population_len
        current_fitness += self.__distance_fitness(mass_centers, area_masses)
        current_fitness += self.__altitude_fitness(height_list)
        current_fitness += self.__amount_fitness(population_len)
        if current_fitness < 0:
            current_fitness = 0
        return current_fitness

    def __size_fitness(self, area_list: list, min_max_values: dict) -> float:
        # Size (dont pick small areas, but also avoid "long small" ones)
        amount_of_blocks = len(area_list)
        # a^2 + b^2 = c^2
        x_distance = min_max_values['max_x'] - min_max_values['min_x']
        z_distance = min_max_values['max_z'] - min_max_values['min_z']
        distance = math.sqrt(math.pow(x_distance, 2) + math.pow(z_distance, 2))
        value = (amount_of_blocks/distance) - self.min_value_for_fitness_distance
        if value <= 0:
            return 0
        else:
            return value * FITNESS_SIZE_VALUE_MULTIPLIER

    def __distance_fitness(self, mass_centers: List[dict], mass_of_areas: List[int]) -> float:
        # Distance to each other (use mass center for all and check distance to average mass center)
        total_distance = 0
        for center, areas_len in zip(mass_centers, mass_of_areas):
            x_distance = center['x'] - self.mass_center['x']
            z_distance = center['z'] - self.mass_center['z']
            # a^2 + b^2 = c^2
            total_distance += (math.sqrt(math.pow(x_distance, 2) + math.pow(z_distance, 2)))/areas_len
        avg_distance = total_distance / len(mass_centers)
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, y2 is 0, x2 is the max distance from each other unless minus)
        # b = max score
        # x = average_distance_to_mass
        a = -FITNESS_DISTANCE_MAX_SCORE / FITNESS_DISTANCE_MAX_ALLOWED_DISTANCE_BEFORE_MINUS
        return a * avg_distance

    def __altitude_fitness(self, height_list: list) -> float:
        # Altitude difference (too much too bad)
        total_difference = 0
        for y in height_list:
            total_difference += self.avg_y - y
        average_difference = total_difference / len(height_list)
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, y2 is 0, x2 is the max y-diff unless minus)
        # b = max score
        # x = average_distance
        a = -FITNESS_ALTITUDE_MAX_SCORE / FITNESS_ALTITUDE_MAX_ALLOWED_DIFFERENCE_BEFORE_MINUS
        return a * average_difference + FITNESS_ALTITUDE_MAX_SCORE

    def __amount_fitness(self, population_len: int) -> float:
        # Amount (should not always go for most districts, but smaller solutions can easily get max score in the other)
        extra_populations = population_len - MIN_AREAS_IN_CITY
        return extra_populations * FITNESS_AMOUNT_BONUS_PER_EXTRA

    # def duplicates_fitness(self, duplicate_areas: dict) -> float:
    #     # Duplicates? (good or bad depending on size)
    #     fitness = FITNESS_DUPLICATE_DEFAULT_SCORE
    #     duplicate_combined_fitness = 0
    #     duplicates_amount = 0
    #     for value in duplicate_areas.values():
    #         if value['repetitions'] > 1:
    #             duplicates_amount += 1
    #             value_should_be_close_to_repetitions = value['length'] / FITNESS_AREA_PER_DISTRICT_FOR_SHARED_SPACE
    #             diff = abs(value_should_be_close_to_repetitions - value['repetitions'])
    #             # 0 is perfect score, anything higher than that should decrease the score
    #             # y = a*x + b
    #             # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, x2 is 0.5, and y2 is 0)
    #             # b = (max score)
    #             # x = difference
    #             a = -FITNESS_DUPLICATE_PERFECT_AMOUNT_SCORE / 0.5
    #             duplicate_combined_fitness += a * diff + FITNESS_DUPLICATE_PERFECT_AMOUNT_SCORE
    #     if duplicates_amount != 0:
    #         fitness += duplicate_combined_fitness / duplicates_amount
    #     return fitness
    #
    #
    # def pillar_fitness(self, area_set: set, min_max_values: dict) -> float:
    #     min_x = min_max_values['min_x']
    #     max_x = min_max_values['max_x']
    #     min_z = min_max_values['min_z']
    #     max_z = min_max_values['max_z']
    #     step_size_x = int(round((max_x-min_x)/2))
    #     step_size_z = int(round((max_z-min_z)/2))
    #     total_possible_pillars = 0
    #     amount_of_pillars_found = 0
    #     for x in range(min_x, max_x, step_size_x):
    #         for z in range(min_z, max_z, step_size_z):
    #             if (x, z) in area_set:
    #                 amount_of_pillars_found += 1
    #             total_possible_pillars += 1
    #     fitness = (FITNESS_PILLAR_MAX_SCORE / total_possible_pillars) * amount_of_pillars_found
    #     return fitness

    # def distance_from_min_to_max_corners(self, min_max_values: dict) -> float:
    #     min_x = min_max_values['min_x']
    #     max_x = min_max_values['max_x']
    #     min_z = min_max_values['min_z']
    #     max_z = min_max_values['max_z']
    #     # a^2 + b^2 = c^2
    #     x_distance = max_x - min_x
    #     z_distance = max_z - min_z
    #     distance = math.sqrt(math.pow(x_distance, 2) + math.pow(z_distance, 2)) - FITNESS_CORNERS_DISTANCE_FOR_MAX_SCORE
    #     if distance <= 0:
    #         return FITNESS_CORNERS_MAX_SCORE
    #     # y = a*x + b
    #     # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, y2 is 0, x2 is the max cut for 0 points)
    #     # b = max score
    #     # x = distance
    #     a = (-FITNESS_CORNERS_MAX_SCORE / FITNESS_ALTITUDE_MAX_ALLOWED_DIFFERENCE_BEFORE_MINUS)
    #     return a * distance + FITNESS_CORNERS_MAX_SCORE
