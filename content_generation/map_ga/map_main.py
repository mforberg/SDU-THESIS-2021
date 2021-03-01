from .map_fitness import MapFitness
from .map_initial_population import MapInitialPopulation
from .map_selection import MapSelection
from .map_crossover import MapCrossover
from .map_mutation import MapMutation
from variables.ga_map_variables import *
from variables.shared_variables import *
import copy


class AreasGA:

    best_solution = SolutionGA(fitness=0, population=[AreaMap(area_type="None", area_set=None, coordinates=None,
                                                              mass_coordinate=None, min_max_values=None, height=None)])
    set_of_population = set()

    def run(self, areas: SolutionGA) -> SolutionGA:
        populations = []
        # Generate initial population
        for i in range(0, MAP_POPULATION_SIZE):
            initial_population = MapInitialPopulation().create(areas)
            populations.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in range(0, MAP_GENERATION_AMOUNT):
            self.set_of_population = set()
            for pop in populations:
                if pop in self.set_of_population:
                    print("oh no")
                self.set_of_population.add(pop)

            print(f"Current generation in Map_GA: {i}, length: {len(populations)}")
            MapFitness().calculate_fitness_for_all(populations)
            self.check_for_new_best_solution(populations)
            # as long as it is not the last generation, find parents, do crossover, and mutate
            if i != MAP_GENERATION_AMOUNT - 1:
                parents_no_fitness = MapSelection().select_best_solutions(populations)
                crossed_population_no_fitness = MapCrossover().crossover(populations, parents_no_fitness)
                MapMutation().mutate_populations(crossed_population_no_fitness, areas)
                populations = crossed_population_no_fitness
        return self.best_solution

    def check_for_new_best_solution(self, populations: List[SolutionGA]):
        for solution in populations:
            if solution.fitness > self.best_solution.fitness:
                self.best_solution = copy.deepcopy(solution)
                print(f"New best {solution.fitness}")
