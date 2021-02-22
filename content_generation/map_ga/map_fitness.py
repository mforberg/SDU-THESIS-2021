import math
import random
from typing import List

from variables.ga_map_variables import *
from variables.map_variables import MIN_SIZE_OF_AREA


class MapFitness:

    mass_center = (0, 0)
    avg_y = 0

    def calculate_fitness_for_all(self, population_list: List[dict], surface_dict: dict, blocks_dict: dict):
        for population in population_list:
            self.calculate_individual_fitness(population)

    def calculate_individual_fitness(self, population_dict: dict):
        self.mass_center = (0, 0)
        self.avg_y = 0
        population_dict['fitness'] = self.calculate_fitness_from_population(population_dict['population'])

    def calculate_fitness_from_population(self, population: list) -> float:
        current_fitness = 0
        mass_centers = []
        height_list = []
        total_x = 0
        total_z = 0
        total_y = 0
        duplicate_areas = {}  # key = mass_coordinate, value = [repetitions, length]
        for area in population:
            if area['mass_coordinate'] in duplicate_areas:
                duplicate_areas[area['mass_coordinate']]['repetitions'] += 1  # should increase repetitions with 1
            else:
                duplicate_areas[area['mass_coordinate']] = {'repetitions': 1, 'length': len(area['area'])}
            current_fitness += self.size_fitness(area['area'])
            mass_centers.append(area['mass_coordinate'])
            height_list.append(area['height'])
            total_x += area['mass_coordinate'][0]
            total_z += area['mass_coordinate'][1]
            total_y += area['height']
        population_len = len(population)
        self.mass_center = (total_x / population_len, total_z / population_len)
        self.avg_y = total_y / population_len
        current_fitness += self.duplicates_fitness(duplicate_areas)
        current_fitness += self.distance_fitness(mass_centers)
        current_fitness += self.altitude_fitness(height_list)
        current_fitness += self.amount_fitness(population_len)
        return current_fitness

    def size_fitness(self, area_list: list) -> float:
        # Size (dont pick small areas)
        length = len(area_list)
        if length >= FITNESS_PERFECT_LENGTH:
            return FITNESS_SIZE_MAX_SCORE
        else:
            # y = a*x + b
            # a = y2 - y1 / x2 - x1 (y1 and x1 is 0, as the formula crosses the coordinate 0,0)
            # b = 0
            # x = length - size that gives 0 point (aka minimum allowed size of an area)
            return (FITNESS_SIZE_MAX_SCORE / FITNESS_PERFECT_LENGTH) * (length - MIN_SIZE_OF_AREA)

    def duplicates_fitness(self, duplicate_areas: dict) -> float:
        # Duplicates? (good or bad depending on size)
        fitness = FITNESS_DUPLICATE_DEFAULT_SCORE
        duplicate_combined_fitness = 0
        duplicates_amount = 0
        for value in duplicate_areas.values():
            if value['repetitions'] > 1:
                duplicates_amount += 1
                value_should_be_close_to_repetitions = value['length'] / FITNESS_AREA_PER_DISTRICT_FOR_SHARED_SPACE
                diff = abs(value_should_be_close_to_repetitions - value['repetitions'])
                # 0 is perfect score, anything higher than that should decrease the score
                # y = a*x + b
                # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, x2 is 0.5, and y2 is 0)
                # b = (max score)
                # x = difference
                a = -FITNESS_DUPLICATE_PERFECT_AMOUNT_SCORE / 0.5
                duplicate_combined_fitness += a * diff + FITNESS_DUPLICATE_PERFECT_AMOUNT_SCORE
        if duplicates_amount != 0:
            fitness += duplicate_combined_fitness / duplicates_amount
        return fitness

    def distance_fitness(self, mass_centers: List[tuple]) -> float:
        # Distance to each other (use mass center for all and check distance to average mass center)
        total_distance = 0
        for center in mass_centers:
            x_distance = center[0] - self.mass_center[0]
            z_distance = center[1] - self.mass_center[1]
            # a^2 + b^2 = c^2
            total_distance += math.sqrt(math.pow(x_distance, 2) + math.pow(z_distance, 2))
        avg_distance = total_distance / len(mass_centers)
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, y2 is 0, x2 is the max distance from each other unless minus)
        # b = max score
        # x = average_distance_to_mass
        a = -FITNESS_DISTANCE_MAX_SCORE / FITNESS_DISTANCE_MAX_ALLOWED_DISTANCE_BEFORE_MINUS
        return a * avg_distance

    def altitude_fitness(self, height_list: list) -> float:
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

    def amount_fitness(self, population_len: int) -> float:
        # Amount (should not always go for most districts, but smaller solutions can easily get max score in the other)
        extra_populations = population_len - MIN_AREAS_IN_CITY
        return extra_populations * FITNESS_AMOUNT_BONUS_PER_EXTRA
