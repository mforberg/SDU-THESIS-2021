import copy
from shared_variables import *

# Map_GA variables
MAP_POPULATION_SIZE = 100
MAP_AMOUNT_OF_PARENTS_CHOSEN = 100  # if this is not the same as MAP_POP_SIZE randoms will be put into the parent list
MIN_AREAS_IN_CITY = 3
MAX_AREAS_IN_CITY = 5
MAP_GENERATION_AMOUNT = 20
MAP_ELITISM_AMOUNT = 10
MAP_MUTATION_PERCENTAGE = 10

# Fitness
#  Size Fitness
FITNESS_PERFECT_LENGTH = 300
FITNESS_SIZE_MAX_SCORE = 500
#  Duplicate Fitness
FITNESS_AREA_PER_DISTRICT_FOR_SHARED_SPACE = 150
FITNESS_DUPLICATE_DEFAULT_SCORE = 100
FITNESS_DUPLICATE_PERFECT_AMOUNT_SCORE = 100
#  Distance Fitness
FITNESS_DISTANCE_MAX_SCORE = 200
FITNESS_DISTANCE_MAX_ALLOWED_DISTANCE_BEFORE_MINUS = 100
#  Altitude Fitness
FITNESS_ALTITUDE_MAX_SCORE = 100
FITNESS_ALTITUDE_MAX_ALLOWED_DIFFERENCE_BEFORE_MINUS = 10
#  Amount Fitness
FITNESS_AMOUNT_BONUS_PER_EXTRA = 10
#  Pillar Fitness
FITNESS_PILLAR_DIVIDE_AMOUNT = 2
FITNESS_PILLAR_MAX_SCORE = 500


class SolutionMap:
    fitness = 0
    population = []

    def __init__(self, fitness, population: List[AreaMap]):
        self.fitness = fitness
        self.population = population

    def __deepcopy__(self, memo):
        copy_list = []
        for x in self.population:
            copy_list.append(copy.deepcopy(x, memo))
        copy_object = SolutionMap(self.fitness, copy_list)
        return copy_object
