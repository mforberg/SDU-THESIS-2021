import random
from variables.ga_type_variables import *
from models.shared_models import *


class TypeSelection:

    def select_best_solutions(self, population_list: List[SolutionGA]):
        parent_list = []
        total_fitness = self.__create_weighted_wheel(population=population_list)
        for i in range(0, TYPE_AMOUNT_OF_PARENTS_CHOSEN):
            parent_list.append(self.__select_solution_for_parent(population_list=population_list,
                                                                 total_fitness=total_fitness))
        random.shuffle(population_list)
        x = 0
        while len(parent_list) < len(population_list):
            parent_list.append(population_list[x])
            x += 1
        return parent_list

    def __create_weighted_wheel(self, population: List[SolutionGA]) -> float:
        total_fitness = 0
        for solution in population:
            total_fitness += solution.fitness
        return total_fitness

    def __select_solution_for_parent(self, population_list: List[SolutionGA], total_fitness: float) -> SolutionGA:
        random_float = random.random()
        fitness_left = random_float * total_fitness
        for i in population_list:
            if i.fitness >= fitness_left:
                return i
            else:
                fitness_left -= i.fitness
