import random

from typing import List

from variables.ga_map_variables import *


class MapMutation:

    areas = []

    def mutate_populations(self, population_list: List[dict], areas: List[List[tuple]]):
        self.areas = areas
        for population in population_list:
            if random.randint(1, 100) > MAP_MUTATION_PERCENTAGE:
                if random.randint(1, 2) == 1:
                    if len(population['population']) < MAX_AREAS_IN_CITY:
                        self.increase_size(population)
                else:
                    if len(population['population']) > MIN_AREAS_IN_CITY:
                        self.decrease_size(population)
            if len(population['population']) > MAX_AREAS_IN_CITY:
                print("mutate problem")

    def increase_size(self, population: dict):
        population["population"].append(self.areas[random.randint(0, len(self.areas) - 1)])
        random.shuffle(population['population'])

    def decrease_size(self, population: dict):
        random.shuffle(population['population'])
        population['population'].pop(0)
