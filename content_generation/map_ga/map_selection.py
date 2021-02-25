import random
from variables.ga_map_variables import *


class MapSelection:
    total_fitness = 0

    def select_best_solutions(self, population_list: List[SolutionMap]) -> List[List[AreaMap]]:
        self.total_fitness = 0
        self.create_weighted_wheel(population_list)
        parent_list = []
        for i in range(0, MAP_AMOUNT_OF_PARENTS_CHOSEN):
            parent_list.append(self.select_solution_for_parent(population_list))
        random.shuffle(population_list)
        counter = 0
        while len(parent_list) < len(population_list):
            # parent_list.append(copy.deepcopy(population_list[counter]['population']))
            parent_list.append(population_list[counter].population)
            counter += 1
        return parent_list

    def create_weighted_wheel(self, total_pop: List[SolutionMap]):
        for solution in total_pop:
            self.total_fitness += solution.fitness

    def select_solution_for_parent(self, population_list: List[SolutionMap]) -> List[AreaMap]:
        random_float = random.random()
        fitness_left = random_float * self.total_fitness
        for population in population_list:
            if population.fitness >= fitness_left:
                # return copy.deepcopy(population['population'])
                return population.population
            else:
                fitness_left -= population.fitness
