import random
from typing import Dict
from variables.ga_type_variables import *
from variables.shared_variables import *


class TypeCrossover:
    parent_list = []

    def crossover(self, population_list: List[SolutionGA], parent_list: List[SolutionGA]) -> List[SolutionGA]:
        self.parent_list = parent_list
        new_population = []
        ordered_population_list = population_list
        ordered_population_list.sort(key=lambda x: x.fitness, reverse=True)
        # pick top x
        i = 0
        for solution in ordered_population_list:
            if i == TYPE_ELITISM_AMOUNT:
                break
            i += 1
            solution.fitness = 0
            new_population.append(copy.deepcopy(solution))
        while len(new_population) < TYPE_POPULATION_SIZE:
            parents = self.find_two_parents()
            children_dict = self.create_offspring(parents['p1'], parents['p2'])
            new_population.append(SolutionGA(fitness=0, population=children_dict['c1']))
            if len(new_population) < TYPE_POPULATION_SIZE:
                new_population.append(SolutionGA(fitness=0, population=children_dict['c2']))
        return new_population

    def find_two_parents(self) -> dict:
        parent1 = self.get_parent()
        parent2 = self.get_parent()
        return {"p1": copy.deepcopy(parent1), "p2": copy.deepcopy(parent2)}

    def get_parent(self) -> SolutionGA:
        random_index = random.randint(0, len(self.parent_list) - 1)
        return copy.deepcopy(self.parent_list[random_index])

    def create_offspring(self, parent1: SolutionGA, parent2: SolutionGA) -> Dict[str, List[SolutionArea]]:
        random.shuffle(parent1.population)
        random.shuffle(parent2.population)
        if len(parent1.population) > len(parent2.population):
            return self.single_point_crossover(shortest=parent2.population, longest=parent1.population)
        else:
            return self.single_point_crossover(shortest=parent1.population, longest=parent2.population)

    def single_point_crossover(self, shortest: List[SolutionArea], longest: List[SolutionArea]) -> Dict[str, List[SolutionArea]]:
        point = random.randint(0, len(shortest)-1)
        child1 = shortest
        child2 = longest
        flip = False
        for i in range(0, len(longest)):
            if i == point:
                flip = True
            if not flip:
                if i < len(shortest):
                    child1[i].type_of_district = shortest[i].type_of_district
                child2[i].type_of_district = longest[i].type_of_district
            else:
                if i < len(shortest):
                    child2[i].type_of_district = shortest[i].type_of_district
                child1[i].type_of_district = longest[i].type_of_district
        return {"c1": child1, "c2": child2}
