import random
from models.shared_models import *


class Selection:

    def __init__(self, amount_of_parents_chosen: int):
        self.total_fitness = 0
        self.amount_of_parents_chosen = amount_of_parents_chosen

    def select_best_solutions(self, population_list: List[SolutionGA]):
        self.total_fitness = 0
        self.__create_weighted_wheel(population=population_list)
        parent_list = []
        for i in range(0, self.amount_of_parents_chosen):
            parent_list.append(self.__select_solution_for_parent(population_list=population_list))
        random.shuffle(population_list)
        x = 0
        while len(parent_list) < len(population_list):
            parent_list.append(population_list[x])
            x += 1
        return parent_list

    def __create_weighted_wheel(self, population: List[SolutionGA]):
        for solution in population:
            self.total_fitness += solution.fitness

    def __select_solution_for_parent(self, population_list: List[SolutionGA]) -> SolutionGA:
        random_float = random.random()
        fitness_left = random_float * self.total_fitness
        for i in population_list:
            if i.fitness >= fitness_left:
                return i
            else:
                fitness_left -= i.fitness
