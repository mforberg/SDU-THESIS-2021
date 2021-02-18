from typing import List

from variables.ga_map_variables import *
import random
import copy


class InitialPopulation:

    def create(self, areas: List[List[tuple]]) -> List[List[tuple]]:
        population = []
        for i in range(0, random.randint(MIN_AREAS_IN_CITY, MAX_AREAS_IN_CITY)):
            population.append(self.pick_random_area(areas))
        return population

    def pick_random_area(self, areas: List[List[tuple]]) -> List[tuple]:
        area = copy.deepcopy(areas[random.randint(0, len(areas)-1)])
        return area
