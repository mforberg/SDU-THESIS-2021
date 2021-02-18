import random
from variables.ga_map_variables import *


class MapFitness:

    def calculate_fitness_for_all(self, population_list: list, surface_dict: dict, blocks_dict: dict):
        for population in population_list:
            self.calculate_individual_fitness(population)

    def calculate_individual_fitness(self, population_dict: dict):
        population_dict['fitness'] = self.calculate_fitness_from_population(population_dict['population'])

    def calculate_fitness_from_population(self, population: list) -> int:
        current_fitness = 0
        checked_areas = set()
        for area in population:
            print(area)
            if area['mass_coordinate'] in checked_areas:
                pass
            if len(area['area']) >= FITNESS_SINGLE_AREA_LIMIT:
                pass

            checked_areas.add(area['mass_coordinate'])
        return random.randint(1, 10000)
