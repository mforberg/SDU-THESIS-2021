from variables.ga_map_variables import *
from variables.shared_variables import *
import random
import copy


class MapInitialPopulation:

    def create(self, areas: SolutionGA) -> SolutionGA:
        initial_solution = SolutionGA(fitness=0, population=[])
        for i in range(0, random.randint(MIN_AREAS_IN_CITY, MAX_AREAS_IN_CITY)):
            initial_solution.population.append(self.__pick_random_area(areas.population))
        return initial_solution

    def __pick_random_area(self, areas: List[SolutionArea]) -> SolutionArea:
        area = copy.deepcopy(areas[random.randint(0, len(areas)-1)])
        return area
