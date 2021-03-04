from variables.shared_variables import *
import random


class TypeFitness:

    surface_dict = {}
    global_dict_of_used_types = {}

    def calculate_fitness_for_all(self, population_list: List[SolutionGA], surface_dict: dict,
                                  global_dict_of_used_types: dict):
        self.surface_dict = surface_dict
        self.global_dict_of_used_types = global_dict_of_used_types
        for solution in population_list:
            self.calculate_individual_fitness(solution=solution)

    def calculate_individual_fitness(self, solution: SolutionGA):
        solution.fitness = random.randint(0, 10000)
