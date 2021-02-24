import random
import copy
from typing import List

from variables.ga_map_variables import *


class MapSelection:
    total_fitness = 0

    def select_best_solutions(self, population_list: List[dict]) -> List[List[tuple]]:
        self.total_fitness = 0
        ordered_population_dict = copy.deepcopy(population_list)
        ordered_population_dict.sort(key=lambda x: x['fitness'], reverse=True)
        self.create_weighted_wheel(ordered_population_dict)
        parent_list = []
        for i in range(0, MAP_AMOUNT_OF_PARENTS_CHOSEN):
            parent_list.append(self.select_solution_for_parent(ordered_population_dict))
        random.shuffle(population_list)
        x = 0
        while len(parent_list) > len(population_list):
            parent_list.append(copy.deepcopy(population_list[x]['population']))
            x += 1
        return parent_list

    def create_weighted_wheel(self, population: List[dict]):
        for solution in population:
            self.total_fitness += solution['fitness']

    def select_solution_for_parent(self, ordered_population_list: List[dict]) -> List[tuple]:
        random_float = random.random()
        fitness_left = random_float * self.total_fitness
        for i in ordered_population_list:
            if i['fitness'] >= fitness_left:
                return copy.deepcopy(i['population'])
            else:
                fitness_left -= i['fitness']
