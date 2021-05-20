import random
from typing import Dict
from variables.ga_type_variables import *
from models.shared_models import *


class Crossover:

    def __init__(self, population_size: int):
        self.parent_list = []
        self.population_size = population_size

    def crossover(self, population_list: List[SolutionGA], parent_list: List[SolutionGA]) -> List[SolutionGA]:
        self.parent_list = parent_list
        new_population = []
        ordered_population_list = population_list
        ordered_population_list.sort(key=lambda x: x.fitness, reverse=True)
        # pick top x
        for i, solution in enumerate(ordered_population_list):
            if i == TYPE_ELITISM_AMOUNT:
                break
            new_solution = copy.deepcopy(solution)
            new_solution.fitness = 0
            new_population.append(new_solution)
        while len(new_population) < self.population_size:
            parents = self.__find_two_parents()
            children_dict = self.__create_offspring(parents['p1'], parents['p2'])
            new_population.append(SolutionGA(fitness=0, population=children_dict['c1']))
            if len(new_population) < self.population_size:
                new_population.append(SolutionGA(fitness=0, population=children_dict['c2']))
        return new_population

    def __find_two_parents(self) -> dict:
        parent1 = self.__get_parent()
        parent2 = self.__get_parent()
        return {"p1": copy.deepcopy(parent1), "p2": copy.deepcopy(parent2)}

    def __get_parent(self) -> SolutionGA:
        random_index = random.randint(0, len(self.parent_list) - 1)
        return copy.deepcopy(self.parent_list[random_index])

    def __create_offspring(self, parent1: SolutionGA, parent2: SolutionGA) -> Dict[str, List[SolutionArea]]:
        random.shuffle(parent1.population)
        random.shuffle(parent2.population)
        if len(parent1.population) > len(parent2.population):
            return self.uniform_crossover(shortest=parent2.population, longest=parent1.population)
        else:
            return self.uniform_crossover(shortest=parent1.population, longest=parent2.population)

    def uniform_crossover(self, shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
        pass
