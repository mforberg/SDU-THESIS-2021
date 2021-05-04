import random
from variables.ga_map_variables import *
from models.shared_models import *


class MapSelection:
    def __init__(self):
        self.total_fitness = 0

    def select_best_solutions(self, population_list: List[SolutionGA]) -> List[SolutionGA]:
        self.total_fitness = 0
        self.__create_weighted_wheel(population_list)
        parent_list = []
        for i in range(0, MAP_AMOUNT_OF_PARENTS_CHOSEN):
            parent_list.append(self.__select_solution_for_parent(population_list))
        random.shuffle(population_list)
        counter = 0
        while len(parent_list) < len(population_list):
            parent_list.append(population_list[counter])
            counter += 1
        return parent_list

    def __create_weighted_wheel(self, total_pop: List[SolutionGA]):
        for solution in total_pop:
            self.total_fitness += solution.fitness

    def __select_solution_for_parent(self, population_list: List[SolutionGA]) -> SolutionGA:
        random_float = random.random()
        fitness_left = random_float * self.total_fitness
        for solution in population_list:
            if solution.fitness >= fitness_left:
                return solution
            else:
                fitness_left -= solution.fitness
