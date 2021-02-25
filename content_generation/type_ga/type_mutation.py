import random
from variables.ga_type_variables import *


class TypeMutation:

    def mutate_populations(self, population_list: List[SolutionType]):
        for solution in population_list:
            if random.randint(1, 100) > TYPE_MUTATION_SOLUTION_PERCENTAGE:
                for area in solution.population:
                    if random.randint(1, 100) > TYPE_MUTATION_AREA_PERCENTAGE:
                        self.mutate_solution(area)

    def mutate_solution(self, area: AreaType):
        area.area_type = TYPES_LIST[random.randint(0, len(TYPES_LIST) - 1)]
