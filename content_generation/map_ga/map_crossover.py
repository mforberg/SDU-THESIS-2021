import random

from Crossover import Crossover
from variables.ga_map_variables import *
from variables.shared_variables import *


class MapCrossover(Crossover):

    def __init__(self, population_size:int):
        super().__init__(population_size)

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
