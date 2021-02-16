import map_initial_population
import map_fitness
import map_selection
import map_crossover
import map_mutation
from ..variables import *
import copy


class DistrictGA:

    best_solution = {"population": None, "fitness": 0}

    def run(self, total_block_dict, total_surface_dict, district_areas):
        populations = []

        # Generate initial population
        for i in range(0, population_size-1):
            initial_population = map_initial_population.InitialPopulation().create(district_areas)
            populations.append({"population": initial_population, "fitness": None})
        # repete fitness calculation and select the best solution overall
        for i in range(0, repetitions-1):
            print("Current generation: ", i)
            map_fitness.MapFitness().calculate_fitness_for_all(populations, total_surface_dict, total_block_dict)
            self.check_for_new_best_solution(populations)
            # if i != repetitions - 1:
            #     map_selection.MapSelection().select_best_solutions(populations)
            #     map_crossover.MapCrossover().crossover(populations)
            #     map_mutation.MapMutation().mutate_populations(populations)
        print(self.best_solution)

    def check_for_new_best_solution(self, populations_dict):
        for solution in populations_dict:
            if solution['fitness'] > self.best_solution['fitness']:
                self.best_solution = copy.deepcopy(solution)
                print("New best ", solution)
