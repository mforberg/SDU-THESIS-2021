import random
from crossover import Crossover
from models.shared_models import *


class TypeCrossover(Crossover):

    def __init__(self, population_size: int):
        super().__init__(population_size)

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

    # def __single_point_crossover(self, shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
    #     point = random.randint(0, len(shortest)-1)
    #     child1 = shortest
    #     child2 = longest
    #     flip = False
    #     for i in range(0, len(longest)):
    #         if i == point:
    #             flip = True
    #         if not flip:
    #             if i < len(shortest):
    #                 child1[i].type_of_district = shortest[i].type_of_district
    #             child2[i].type_of_district = longest[i].type_of_district
    #         else:
    #             if i < len(shortest):
    #                 child2[i].type_of_district = shortest[i].type_of_district
    #             child1[i].type_of_district = longest[i].type_of_district
    #     return {"c1": child1, "c2": child2}