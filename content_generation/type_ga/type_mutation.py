import random
from variables.ga_type_variables import *
from variables.map_shared_variables import *


class TypeMutation:

    def mutate_populations(self, population_list: List[SolutionGA]):
        for solution in population_list:
            if random.randint(1, 100) > TYPE_MUTATION_SOLUTION_PERCENTAGE:
                for area in solution.population:
                    if random.randint(1, 100) > TYPE_MUTATION_AREA_PERCENTAGE:
                        self.mutate_solution(area)

    def mutate_solution(self, area: AreaMap):
        area.area_type = DISTRICT_TYPES[random.randint(0, len(DISTRICT_TYPES) - 1)]
