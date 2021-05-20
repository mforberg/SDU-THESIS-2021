import random
from variables.ga_map_variables import *
from models.shared_models import *


class MapMutation:

    def mutate_populations(self, population_list: List[SolutionGA], areas: SolutionGA):
        for solution in population_list:
            if random.randint(1, 100) <= MAP_MUTATION_PERCENTAGE:
                if random.randint(1, 2) == 1:
                    if len(solution.population) < MAX_AREAS_IN_CITY:
                        self.__increase_size(solution.population, areas=areas)
                else:
                    if len(solution.population) > MIN_AREAS_IN_CITY:
                        self.decrease_size(solution.population)

    def __increase_size(self, population: List[SolutionArea], areas: SolutionGA):
        no_new_area = True
        while no_new_area:
            random_area = areas.population[random.randint(0, len(areas.population) - 1)]
            if random_area not in population:
                no_new_area = False
                population.append(random_area)
        random.shuffle(population)

    def decrease_size(self, population: List[SolutionArea]):
        random.shuffle(population)
        population.pop(0)
