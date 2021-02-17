from .map_fitness import MapFitness
from .map_initial_population import InitialPopulation
from .map_selection import MapSelection
from .map_crossover import MapCrossover
from .map_mutation import MapMutation
from variables.ga_map_variables import *
import copy


class DistrictGA:

    best_solution = {"population": None, "fitness": 0}

    def run(self, total_block_dict, total_surface_dict, district_areas):
        populations = []
        # Generate initial population
        for i in range(0, POPULATION_SIZE):
            initial_population = InitialPopulation().create(district_areas)
            populations.append({"population": initial_population, "fitness": None})
        # repeat fitness calculation and select the best solution overall
        for i in range(0, REPETITIONS):
            print(f"Current generation: {i}")
            MapFitness().calculate_fitness_for_all(populations, total_surface_dict, total_block_dict)
            self.check_for_new_best_solution(populations)
            if i != REPETITIONS - 1:
                parents = MapSelection().select_best_solutions(populations)
                new_population = MapCrossover().crossover(populations, parents)
                print(new_population)
            #     MapMutation().mutate_populations(populations)
        print(self.best_solution)

    def check_for_new_best_solution(self, populations_dict):
        for solution in populations_dict:
            if solution['fitness'] > self.best_solution['fitness']:
                self.best_solution = copy.deepcopy(solution)
                print(f"New best {solution}")
