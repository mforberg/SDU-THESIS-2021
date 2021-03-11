import shared_variables
from typing import List

DISTRICT_TYPES = ["Fishing", "Trade", "Royal", "Farms", "Crafts", "Village"]

# Type_GA variables
TYPE_POPULATION_SIZE = 200
TYPE_AMOUNT_OF_PARENTS_CHOSEN = 200  # if this is not the same as TYPE_POP_SIZE randoms will be put into the parent list
TYPE_GENERATION_AMOUNT = 20
TYPE_ELITISM_AMOUNT = 20
TYPE_MUTATION_SOLUTION_PERCENTAGE = 10
TYPE_MUTATION_AREA_PERCENTAGE = 20

# PreProcess:
TYPE_AREA_AROUND_DISTRICT_TO_BE_CHECKED = 10

# Fitness
#  Checking for new duplicates:
FITNESS_TYPE_DUPLICATES_MAX_SCORE = 100
FITNESS_TYPE_DUPLICATES_AMOUNT_BEFORE_MINUS = 2
#  Fishing district:
FITNESS_TYPE_FISHING_MAX_SCORE = 100
FITNESS_TYPE_FISHING_PERFECT_WATER_PER_BLOCK = 0.4
#  Royal district:
FITNESS_TYPE_ROYAL_MAX_SCORE = 100
FITNESS_TYPE_ROYAL_DISTANCE_FROM_CITY_CENTER_BEFORE_MINUS = 50
#  Crafting district:
FITNESS_TYPE_CRAFTING_MAX_SCORE = 100
FITNESS_TYPE_CRAFTING_PERFECT_RESOURCE_PER_BLOCK = 0.2
#  Default districts: (as to avoid the other types to dominate)
FITNESS_TYPE_DEFAULT_SCORE = 50


class PreProcessData:

    def __init__(self, water_list: List[tuple], resource_list: List[tuple]):
        self.water_list = water_list
        self.resource_list = resource_list
        self.water_mass = shared_variables.calculate_mass_coordinate(water_list)
        self.resource_mass = shared_variables.calculate_mass_coordinate(resource_list)


# class AreaType:
#     area_type = ""
#     list_of_coordinates = []
#
#     def __init__(self, area_type: str, coordinates: List[list]):
#         self.area_type = area_type
#         self.list_of_coordinates = coordinates
#
#     def __deepcopy__(self, memo):
#         copy_object = AreaType(self.area_type, self.list_of_coordinates)
#         return copy_object
#
#
# class SolutionType:
#     fitness = 0
#     amount = 0
#     population = []
#
#     def __init__(self, fitness, population: List[AreaType], amount):
#         self.fitness = fitness
#         self.population = population
#         self.amount = amount
#
#     def __deepcopy__(self, memo):
#         copy_list = []
#         for x in self.population:
#             copy_list.append(copy.deepcopy(x, memo))
#         copy_object = SolutionType(self.fitness, copy_list, self.amount)
#         return copy_object
