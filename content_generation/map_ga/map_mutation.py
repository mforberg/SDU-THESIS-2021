import random
from variables.ga_map_variables import *


class MapMutation:

    district_areas = []

    def mutate_populations(self, population_list, district_areas):
        self.district_areas = district_areas
        for population in population_list:
            if random.randint(1, 100) > MUTATION_PERCENTAGE:
                if random.randint(1, 2) == 1:
                    self.increase_size(population)
                else:
                    self.decrease_size(population)

    def increase_size(self, population):
        random.shuffle(population)
        population.append(self.district_areas[random.randint(0, len(self.district_areas) - 1)])

    def decrease_size(self, population):
        random.shuffle(population)
        population.pop(0)
