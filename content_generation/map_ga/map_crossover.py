import random
from variables.ga_map_variables import *
from variables.map_shared_variables import *


class MapCrossover:
    parent_list = []

    def crossover(self, population_list: List[SolutionGA], parent_list: List[List[AreaMap]]) -> List[SolutionGA]:
        self.parent_list = parent_list
        new_population = []
        ordered_population_list = population_list
        ordered_population_list.sort(key=lambda x: x.fitness, reverse=True)
        # pick top x
        i = 0
        for solution in ordered_population_list:
            if i == MAP_ELITISM_AMOUNT:
                break
            i += 1
            new_population.append(copy.deepcopy(solution))
        while len(new_population) < MAP_POPULATION_SIZE:
            parents = self.find_two_parents()
            result = self.create_offspring(parents['p1'], parents['p2'])
            new_population.append(SolutionGA(fitness=0, population=result['c1']))
            if len(new_population) < MAP_POPULATION_SIZE:
                new_population.append(SolutionGA(fitness=0, population=result['c2']))
        return new_population

    def find_two_parents(self) -> dict:
        parent1 = self.get_parent()
        parent2 = self.get_parent()
        return {"p1": copy.deepcopy(parent1), "p2": copy.deepcopy(parent2)}

    def get_parent(self) -> List[AreaMap]:
        random_index = random.randint(0, len(self.parent_list) - 1)
        return copy.deepcopy(self.parent_list[random_index])

    def create_offspring(self, parent1: List[AreaMap], parent2: List[AreaMap]) -> dict:
        random.shuffle(parent1)
        random.shuffle(parent2)
        if len(parent1) > len(parent2):
            return self.single_point_crossover(shortest=parent2, longest=parent1)
        else:
            return self.single_point_crossover(shortest=parent1, longest=parent2)

    def single_point_crossover(self, shortest: List[AreaMap], longest: List[AreaMap]) -> dict:
        point = random.randint(0, len(shortest)-1)
        child1 = []
        child2 = []
        flip = False
        for i in range(0, len(longest)):
            if i == point:
                flip = True
            if not flip:
                if i < len(shortest):
                    child1.append(shortest[i])
                child2.append(longest[i])
            else:
                if i < len(shortest):
                    child2.append(shortest[i])
                child1.append(longest[i])
        return {"c1": child1, "c2": child2}
