from typing import List

TYPES_LIST = ["Fishing", "Trade", "Royal", "Farms", "Crafts", "Village"]

# Type_GA variables
TYPE_POPULATION_SIZE = 100
TYPE_AMOUNT_OF_PARENTS_CHOSEN = 100  # if this is not the same as TYPE_POP_SIZE randoms will be put into the parent list
TYPE_GENERATION_AMOUNT = 20
TYPE_ELITISM_AMOUNT = 10
TYPE_MUTATION_PERCENTAGE = 10


class Area:
    area_type = ""
    list_of_coordinates = []

    def __init__(self, area_type: str, coordinates: List[tuple]):
        self.area_type = area_type
        self.list_of_coordinates = coordinates


class Solution:
    fitness = 0
    population = []

    def __init__(self, fitness, population: List[Area]):
        self.fitness = fitness
        self.population = population
