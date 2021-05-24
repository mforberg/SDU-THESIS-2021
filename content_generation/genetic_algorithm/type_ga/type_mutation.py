import random
from variables.ga_type_variables import *
from models.shared_models import *


class TypeMutation:

    def mutate_populations(self, population_list: List[SolutionGA]):
        for solution in population_list:
            if random.randint(1, 100) <= TYPE_MUTATION_SOLUTION_PERCENTAGE:
                for area in solution.population:
                    if random.randint(1, 100) <= TYPE_MUTATION_AREA_PERCENTAGE:
                        self.__mutate_solution(area)

    def __mutate_solution(self, area: SolutionArea):
        area.area_type = DISTRICT_TYPES[random.randint(0, len(DISTRICT_TYPES) - 1)]
