import random
from variables.ga_map_variables import *
from variables.shared_variables import *


class MapCrossover:

    def __init__(self):
        self.parent_list = []
        self.work = []

    def crossover(self, population_list: List[SolutionGA], parent_list: List[List[SolutionArea]]) -> List[SolutionGA]:
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
            parents = self.__find_two_parents()
            result = self.create_offspring(parents['p1'], parents['p2'])
            new_population.append(SolutionGA(fitness=0, population=result['c1']))
            if len(new_population) < MAP_POPULATION_SIZE:
                new_population.append(SolutionGA(fitness=0, population=result['c2']))
        return new_population

    def __find_two_parents(self) -> dict:
        parent1 = self.__get_parent()
        parent2 = self.__get_parent()
        return {"p1": copy.deepcopy(parent1), "p2": copy.deepcopy(parent2)}

    def __get_parent(self) -> List[SolutionArea]:
        random_index = random.randint(0, len(self.parent_list) - 1)
        return copy.deepcopy(self.parent_list[random_index])

    def create_offspring(self, parent1: List[SolutionArea], parent2: List[SolutionArea]) -> dict:
        random.shuffle(parent1)
        random.shuffle(parent2)
        if len(parent1) > len(parent2):
            return self.uniform_crossover(shortest=parent2, longest=parent1)
        else:
            return self.uniform_crossover(shortest=parent1, longest=parent2)

    # def k_point_crossover(self, k: int, shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
    #     points = set()
    #     while len(shortest) > len(points) and k >= len(points):
    #         new_value = False
    #         while not new_value:
    #             point = random.randint(0, len(shortest) - 1)
    #             if point not in points:
    #                 new_value = True
    #                 points.add(point)
    #     child1 = []
    #     child2 = []
    #     flip = False
    #     for i in range(0, len(longest)):
    #         if i in points:
    #             flip = not flip
    #         if not flip:
    #             if i < len(shortest):
    #                 child1.append(shortest[i])
    #             child2.append(longest[i])
    #         else:
    #             if i < len(shortest):
    #                 child2.append(shortest[i])
    #             child1.append(longest[i])
    #     return {"c1": child1, "c2": child2}

    def uniform_crossover(self, shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
        child1 = []
        child2 = []
        for i in range(0, len(longest)):
            if random.randint(0, 1) == 0:
                if i < len(shortest):
                    child1.append(shortest[i])
                child2.append(longest[i])
            else:
                if i < len(shortest):
                    child2.append(shortest[i])
                child1.append(longest[i])
        return {"c1": child1, "c2": child2}
