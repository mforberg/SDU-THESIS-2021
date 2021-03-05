from variables.shared_variables import *
from variables.ga_type_variables import *


class TypeFitness:

    surface_dict = {}
    global_dict_of_used_types = {}

    def calculate_fitness_for_all(self, population_list: List[SolutionGA], surface_dict: dict,
                                  global_dict_of_used_types: dict, preprocess_dict: dict):
        self.surface_dict = surface_dict
        self.global_dict_of_used_types = global_dict_of_used_types
        for solution in population_list:
            self.calculate_individual_fitness(solution=solution, preprocess_dict=preprocess_dict)

    # DISTRICT_TYPES = ["Fishing", "Trade", "Royal", "Farms", "Crafts", "Village"]
    def calculate_individual_fitness(self, solution: SolutionGA, preprocess_dict: dict):
        score = 0
        per_area_fitness = 0
        score += self.score_for_global_districts(solution=solution)
        for area in solution.population:
            if area.type_of_district == "Fishing":
                per_area_fitness += self.fishing_should_be_near_water(area=area, preprocess_dict=preprocess_dict)
        solution.fitness = score

    def fishing_should_be_near_water(self, area: SolutionArea, preprocess_dict: dict):
        water_amount = preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])]
        fitness = water_amount * FITNESS_TYPE_FISHING_BONUS_FOR_WATER_BLOCKS
        return fitness

    def score_for_global_districts(self, solution: SolutionGA) -> float:
        total_type_dict = copy.deepcopy(self.global_dict_of_used_types)
        new_duplicates = 0
        for area in solution.population:
            if area.type_of_district in total_type_dict:
                total_type_dict[area.type_of_district] += 1
                new_duplicates += 1
            else:
                total_type_dict[area.type_of_district] = 1
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, y2 is 0, x2 is the max of duplicates before minus)
        # b = max score
        # x = average_distance_to_mass
        a = (-FITNESS_TYPE_DUPLICATES_MAX_SCORE / FITNESS_TYPE_DUPLICATES_AMOUNT_BEFORE_MINUS)
        return (a * new_duplicates) + FITNESS_TYPE_DUPLICATES_MAX_SCORE
