import random
from variables.ga_map_variables import *
from variables.shared_variables import *


class MapSelection:
    def __init__(self):
        self.total_fitness = 0

    def select_best_solutions(self, population_list: List[SolutionGA]) -> List[List[SolutionArea]]:
        self.total_fitness = 0
        self.__create_weighted_wheel(population_list)
        parent_list = []
        for i in range(0, MAP_AMOUNT_OF_PARENTS_CHOSEN):
            parent_list.append(self.__select_solution_for_parent(population_list))
        random.shuffle(population_list)
        counter = 0
        while len(parent_list) < len(population_list):
            parent_list.append(population_list[counter].population)
            counter += 1
        return parent_list

    def __create_weighted_wheel(self, total_pop: List[SolutionGA]):
        for solution in total_pop:
            self.total_fitness += solution.fitness

    def __select_solution_for_parent(self, population_list: List[SolutionGA]) -> List[SolutionArea]:
        random_float = random.random()
        fitness_left = random_float * self.total_fitness
        for population in population_list:
            if population.fitness >= fitness_left:
                return population.population
            else:
                fitness_left -= population.fitness
