from variables.shared_variables import *
from variables.ga_type_variables import *
import math


class TypeFitness:

    surface_dict = {}
    global_dict_of_used_types = {}

    def calculate_fitness_for_all(self, population_list: List[SolutionGA], surface_dict: dict,
                                  global_dict_of_used_types: dict, preprocess_dict: dict):
        self.surface_dict = surface_dict
        self.global_dict_of_used_types = global_dict_of_used_types
        for solution in population_list:
            self.__calculate_individual_fitness(solution=solution, preprocess_dict=preprocess_dict)

    # DISTRICT_TYPES = ["Fishing", "Trade", "Royal", "Farms", "Crafts", "Village"]
    def __calculate_individual_fitness(self, solution: SolutionGA, preprocess_dict: dict):
        score = 0
        per_area_fitness = 0
        score += self.__avoid_duplicates_global(solution=solution)
        for area in solution.population:
            if area.type_of_district == "Fishing":
                per_area_fitness += self.__fishing_should_be_near_water(area=area, preprocess_dict=preprocess_dict)
            elif area.type_of_district == "Royal":
                per_area_fitness += self.__royal_should_be_close_to_center(area=area, preprocess_dict=preprocess_dict)
            elif area.type_of_district == "Crafts":
                per_area_fitness += self.__crafting_has_resources_nearby(area=area, preprocess_dict=preprocess_dict)
            else:
                per_area_fitness += FITNESS_TYPE_DEFAULT_SCORE
        score += per_area_fitness / len(solution.population)
        if score < 0:
            score = 0
        solution.fitness = score

    def __crafting_has_resources_nearby(self, area: SolutionArea, preprocess_dict: dict) -> float:
        resource_list = preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])].resource_list
        water_mass = preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])].resource_mass
        resource_amount = len(resource_list)
        if resource_amount <= 0:
            return -FITNESS_TYPE_CRAFTING_MAX_SCORE
        resource_per_block = len(area.list_of_coordinates) / resource_amount
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is 0, x1 is 0, y2 is max score, x2 is the perfect amount of resources per block)
        # b = 0
        # x = actual resource per block
        a = FITNESS_TYPE_CRAFTING_MAX_SCORE / FITNESS_TYPE_CRAFTING_PERFECT_RESOURCE_PER_BLOCK
        fitness = a * resource_per_block
        if fitness > FITNESS_TYPE_CRAFTING_MAX_SCORE:
            return FITNESS_TYPE_CRAFTING_MAX_SCORE
        return fitness

    def __royal_should_be_close_to_center(self, area: SolutionArea, preprocess_dict: dict) -> float:
        x_difference = area.mass_coordinate['x'] - preprocess_dict['city_center']['x']
        z_difference = area.mass_coordinate['z'] - preprocess_dict['city_center']['z']
        distance = math.sqrt(math.pow(x_difference, 2) + math.pow(z_difference, 2))
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is max score, x1 is 0, y2 is 0, x2 is the max distance before minus)
        # b = max score
        # x = distance
        a = -FITNESS_TYPE_ROYAL_MAX_SCORE / FITNESS_TYPE_ROYAL_DISTANCE_FROM_CITY_CENTER_BEFORE_MINUS
        return (a * distance) + FITNESS_TYPE_ROYAL_MAX_SCORE

    def __fishing_should_be_near_water(self, area: SolutionArea, preprocess_dict: dict) -> float:
        water_list = preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])].water_list
        water_mass = preprocess_dict[(area.mass_coordinate['x'], area.mass_coordinate['z'])].water_mass
        water_amount = len(water_list)
        if water_amount == 0:
            return -FITNESS_TYPE_FISHING_MAX_SCORE
        water_per_block = len(area.list_of_coordinates) / water_amount
        # y = a*x + b
        # a = y2 - y1 / x2 - x1 (y1 is 0, x1 is 0, y2 is max score, x2 is the perfect amount of water per block)
        # b = 0
        # x = actual water per block
        a = FITNESS_TYPE_FISHING_MAX_SCORE / FITNESS_TYPE_FISHING_PERFECT_WATER_PER_BLOCK
        fitness = a * water_per_block
        if fitness > FITNESS_TYPE_FISHING_MAX_SCORE:
            return FITNESS_TYPE_FISHING_MAX_SCORE
        return fitness

    def __avoid_duplicates_global(self, solution: SolutionGA) -> float:
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
        # x = new_duplicates
        a = -FITNESS_TYPE_DUPLICATES_MAX_SCORE / FITNESS_TYPE_DUPLICATES_AMOUNT_BEFORE_MINUS
        return (a * new_duplicates) + FITNESS_TYPE_DUPLICATES_MAX_SCORE
