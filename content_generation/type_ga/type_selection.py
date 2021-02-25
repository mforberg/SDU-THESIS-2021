import random
from variables.ga_type_variables import *


class TypeSelection:

    def select_best_solutions(self, population_list: List[SolutionType]):
        parent_list = []
        total_fitness = self.create_weighted_wheel(population=population_list)
        for i in range(0, TYPE_AMOUNT_OF_PARENTS_CHOSEN):
            parent_list.append(self.select_solution_for_parent(population_list=population_list,
                                                               total_fitness=total_fitness))
        random.shuffle(population_list)
        x = 0
        while len(parent_list) < len(population_list):
            parent_list.append(population_list[x])
            x += 1
        return parent_list

    def create_weighted_wheel(self, population: List[SolutionType]) -> float:
        total_fitness = 0
        for solution in population:
            total_fitness += solution.fitness
        return total_fitness

    def select_solution_for_parent(self, population_list: List[SolutionType], total_fitness: float) -> SolutionType:
        random_float = random.random()
        fitness_left = random_float * total_fitness
        for i in population_list:
            if i.fitness >= fitness_left:
                return i
            else:
                fitness_left -= i.fitness
