from variables.ga_map_variables import *
from models.shared_models import *
import random
import copy


class MapInitialPopulation:

    def create(self, areas: SolutionGA) -> SolutionGA:
        initial_solution = SolutionGA(fitness=0, population=[])
        for i in range(0, random.randint(MIN_AREAS_IN_CITY, MAX_AREAS_IN_CITY)):
            if i < len(areas.population):
                no_new_area = True
                while no_new_area:
                    random_area = self.__pick_random_area(areas=areas.population)
                    if random_area not in initial_solution.population:
                        no_new_area = False
                        initial_solution.population.append(random_area)
            else:
                break
        return initial_solution

    def __pick_random_area(self, areas: List[SolutionArea]) -> SolutionArea:
        area = copy.deepcopy(areas[random.randint(0, len(areas)-1)])
        return area
