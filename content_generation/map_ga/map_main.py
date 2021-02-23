from typing import List

from .map_fitness import MapFitness
from .map_initial_population import MapInitialPopulation
from .map_selection import MapSelection
from .map_crossover import MapCrossover
from .map_mutation import MapMutation
from variables.ga_map_variables import *
import copy


class AreasGA:

    best_solution = {"population": None, "fitness": 0}

    def run(self, areas: List[List[tuple]]) -> dict:
        populations = []
        # Generate initial population
        for i in range(0, POPULATION_SIZE):
            initial_population = MapInitialPopulation().create(areas)
            populations.append({"population": initial_population})
        # repeat fitness calculation and select the best solution overall
        for i in range(0, GENERATION_AMOUNT):
            print(f"Current generation: {i}")
            MapFitness().calculate_fitness_for_all(populations)
            self.check_for_new_best_solution(populations)
            if i != GENERATION_AMOUNT - 1:
                parents_no_fitness = MapSelection().select_best_solutions(populations)
                crossed_population_no_fitness = MapCrossover().crossover(populations, parents_no_fitness)
                MapMutation().mutate_populations(crossed_population_no_fitness, areas)
                populations = crossed_population_no_fitness
        return self.best_solution

    def check_for_new_best_solution(self, populations_dict):
        for solution in populations_dict:
            if solution['fitness'] > self.best_solution['fitness']:
                self.best_solution = copy.deepcopy(solution)
                print(f"New best {solution['fitness']}")
