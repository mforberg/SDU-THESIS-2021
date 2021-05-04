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
