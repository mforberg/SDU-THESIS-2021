import random
import copy
from typing import List

from variables.ga_type_variables import *


class TypeInitialPopulation:

    def create(self, areas: List[List[tuple]]) -> List[dict]:
        population = []
        for x in range(len(areas)):
            area_type = self.get_random_type()
            population.append({'population': copy.deepcopy(areas[x]), 'type': area_type})
        return population

    def get_random_type(self) -> str:
        random_index = random.randint(0, len(TYPES_LIST) - 1)
        return TYPES_LIST[random_index]
