import random
# from variables.shared_variables import *
from variables.ga_type_variables import *


class TypeInitialPopulation:

    def create(self, clusters: List[List[list]]) -> SolutionType:
        list_of_area = []
        for cluster in clusters:
            area_type = self.get_random_type()
            current_area = AreaType(area_type=area_type, coordinates=cluster)
            list_of_area.append(current_area)
        return SolutionType(fitness=0, population=list_of_area, amount=1)

    def get_random_type(self) -> str:
        random_index = random.randint(0, len(DISTRICT_TYPES) - 1)
        return DISTRICT_TYPES[random_index]
