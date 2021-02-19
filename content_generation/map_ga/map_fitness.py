import random
from typing import List

from variables.ga_map_variables import *
from variables.map_variables import MIN_SIZE_OF_AREA


class MapFitness:

    def calculate_fitness_for_all(self, population_list: List[dict], surface_dict: dict, blocks_dict: dict):
        for population in population_list:
            self.calculate_individual_fitness(population)

    def calculate_individual_fitness(self, population_dict: dict):
        population_dict['fitness'] = self.calculate_fitness_from_population(population_dict['population'])

    def calculate_fitness_from_population(self, population: list) -> int:
        current_fitness = 0
        duplicate_areas = {} # key = mass_coordinate, value = [repetitions, length]
        for area in population:
            if area['mass_coordinate'] in duplicate_areas:
                duplicate_areas[area['mass_coordinate']]['repetitions'] += 1  # should increase repetitions with 1
            else:
                duplicate_areas[area['mass_coordinate']] = {'repetitions': 1, 'length': len(area['area'])}
        return random.randint(1, 10000)

    def size_fitness(self, area_list: list) -> int:
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

    def duplicates_fitness(self, duplicate_areas: dict):
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
        fitness += duplicate_combined_fitness / duplicates_amount
        return fitness

    def distance_fitness(self):
        # Distance to each other (create mass center for all and check distance to all districts)
        pass

    def altitude_fitness(self):
        # Altitude difference (too much too bad)
        pass

    def amount_fitness(self):
        # Amount (should not always go for most districts)
        pass
