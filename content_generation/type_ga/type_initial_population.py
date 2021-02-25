import random

from variables.ga_type_variables import *


class TypeInitialPopulation:

    def create(self, districts: List[List[tuple]]) -> Solution:
        list_of_area = []
        for district in districts:
            area_type = self.get_random_type()
            current_area = Area(area_type=area_type, coordinates=district)
            list_of_area.append(current_area)
        return Solution(fitness=0, population=list_of_area)

    def get_random_type(self) -> str:
        random_index = random.randint(0, len(TYPES_LIST) - 1)
        return TYPES_LIST[random_index]
