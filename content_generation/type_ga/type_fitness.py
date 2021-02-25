from typing import List
from variables.ga_type_variables import *
import random


class TypeFitness:

    def calculate_fitness_for_all(self, population_list: List[SolutionType]):
        for solution in population_list:
            self.calculate_individual_fitness(solution=solution)

    def calculate_individual_fitness(self, solution: SolutionType):
        solution.fitness = random.randint(0, 10000)
