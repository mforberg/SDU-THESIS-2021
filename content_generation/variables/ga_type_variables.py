DISTRICT_TYPES = ["Fishing", "Trade", "Royal", "Farms", "Crafts", "Village"]

# Type_GA variables
TYPE_POPULATION_SIZE = 200
TYPE_AMOUNT_OF_PARENTS_CHOSEN = 200  # if this is not the same as TYPE_POP_SIZE randoms will be put into the parent list
TYPE_GENERATION_AMOUNT = 20
TYPE_ELITISM_AMOUNT = 20
TYPE_MUTATION_SOLUTION_PERCENTAGE = 10
TYPE_MUTATION_AREA_PERCENTAGE = 20


# class AreaType:
#     area_type = ""
#     list_of_coordinates = []
#
#     def __init__(self, area_type: str, coordinates: List[tuple]):
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
#     population = []
#
#     def __init__(self, fitness, population: List[AreaType]):
#         self.fitness = fitness
#         self.population = population
#
#     def __deepcopy__(self, memo):
#         copy_list = []
#         for x in self.population:
#             copy_list.append(copy.deepcopy(x, memo))
#         copy_object = SolutionType(self.fitness, copy_list)
#         return copy_object
