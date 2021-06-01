import random
from crossover import Crossover
from ga_type_variables import TYPE_ELITISM_AMOUNT
from models.shared_models import *


class TypeCrossover(Crossover):

    def __init__(self, population_size: int):
        super().__init__(population_size)
        self.elitism_amount = TYPE_ELITISM_AMOUNT

    def uniform_crossover(self, shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
        child1 = shortest
        child2 = longest
        for i in range(0, len(longest)):
            if random.randint(0, 1) == 0:
                if i < len(shortest):
                    child1[i].type_of_district = shortest[i].type_of_district
                child2[i].type_of_district = longest[i].type_of_district
            else:
                if i < len(shortest):
                    child2[i].type_of_district = shortest[i].type_of_district
                child1[i].type_of_district = longest[i].type_of_district
        return {"c1": child1, "c2": child2}
