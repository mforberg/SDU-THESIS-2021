from .map_fitness import MapFitness
from .map_initial_population import MapInitialPopulation
from .map_selection import MapSelection
from .map_crossover import MapCrossover
from .map_mutation import MapMutation
from variables.ga_map_variables import *
from map_variables import *
import copy


class AreasGA:

    best_solution = SolutionMap(fitness=0, population=[AreaMap(area_type="None", area_set=None, coordinates=None,
                                                               mass_coordinate=None, min_max_values=None, height=None)])

    def run(self, areas: SolutionMap) -> SolutionMap:
        populations = []
        # Generate initial population
        for i in range(0, MAP_POPULATION_SIZE):
            initial_population = MapInitialPopulation().create(areas)
            populations.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in range(0, MAP_GENERATION_AMOUNT):
            print(f"Current generation in Map_GA: {i}")
            MapFitness().calculate_fitness_for_all(populations)
            self.check_for_new_best_solution(populations)
            # as long as it is not the last generation, find parents, do crossover, and mutate
            if i != MAP_GENERATION_AMOUNT - 1:
                parents_no_fitness = MapSelection().select_best_solutions(populations)
                crossed_population_no_fitness = MapCrossover().crossover(populations, parents_no_fitness)
                populations = MapMutation().mutate_populations(crossed_population_no_fitness, areas)
        return self.best_solution

    def check_for_new_best_solution(self, populations: List[SolutionMap]):
        for solution in populations:
            if solution.fitness > self.best_solution.fitness:
                self.best_solution = copy.deepcopy(solution)
                print(f"New best {solution.fitness}")
