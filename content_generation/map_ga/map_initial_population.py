from variables.ga_map_variables import *
import random
import copy


class InitialPopulation:

    def create(self, areas):
        population = []
        for i in range(0, random.randint(MIN_DISTRICTS_IN_CITY, MAX_DISTRICTS_IN_CITY)):
            population.append(self.pick_random_area(areas))
        return population

    def pick_random_area(self, areas):
        area = copy.deepcopy(areas[random.randint(0, len(areas)-1)])
        return area
