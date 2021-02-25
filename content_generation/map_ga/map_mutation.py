import random

from typing import List

from variables.ga_map_variables import *


class MapMutation:

    areas = []

    def mutate_populations(self, population_list: List[List[AreaMap]], areas: SolutionMap) -> List[SolutionMap]:
        self.areas = areas
        list_of_solutions = []
        for population in population_list:
            if random.randint(1, 100) > MAP_MUTATION_PERCENTAGE:
                if random.randint(1, 2) == 1:
                    if len(population) < MAX_AREAS_IN_CITY:
                        self.increase_size(population)
                else:
                    if len(population) > MIN_AREAS_IN_CITY:
                        self.decrease_size(population)
            list_of_solutions.append(SolutionMap(fitness=0, population=population))
        return list_of_solutions


    def increase_size(self, population: List[AreaMap]):
        population.append(self.areas.population[random.randint(0, len(self.areas.population) - 1)])
        random.shuffle(population)

    def decrease_size(self, population: List[AreaMap]):
        random.shuffle(population)
        population.pop(0)
