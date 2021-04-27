from .map_fitness import MapFitness
from .map_initial_population import MapInitialPopulation
from .map_selection import MapSelection
from .map_crossover import MapCrossover
from .map_mutation import MapMutation
from variables.ga_map_variables import *
from variables.shared_variables import *
from tqdm import trange


class AreasGA:

    def __init__(self):
        self.best_solution = SolutionGA(fitness=0, population=[SolutionArea(coordinates=[], mass_coordinate={},
                                                                            min_max_values={}, height=0,
                                                                            type_of_district="no")])
        self.set_of_population = set()
        self.population_averages = []
        self.new_best_prints = []
        self.DFC = DataFileCreator(filename="map_ga_data")

    def run(self, areas: SolutionGA) -> SolutionGA:
        population = []
        # Generate initial population
        for i in range(0, MAP_POPULATION_SIZE):
            initial_population = MapInitialPopulation().create(areas)
            population.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in trange(MAP_GENERATION_AMOUNT, desc='GA for finding areas', leave=True):
            #  Fitness
            MapFitness().calculate_fitness_for_all(population)
            r = self.DFC.check_stats_on_solution(population=population, current_gen=i, best_solution=self.best_solution)
            self.new_best_prints.extend(r[0])
            self.best_solution = r[1]
            # as long as it is not the last generation, find parents, do crossover, and mutate
            if i != MAP_GENERATION_AMOUNT - 1:
                #  Select
                parents_no_fitness = MapSelection().select_best_solutions(population)
                #  Crossover
                crossed_population_no_fitness = MapCrossover().crossover(population, parents_no_fitness)
                #  Mutation
                MapMutation().mutate_populations(crossed_population_no_fitness, areas)
                #  set population and clean it
                population = crossed_population_no_fitness
                self.__clean_population_for_duplicates_in_solution(population=population)
        for string in self.new_best_prints:
            print(string)
        return self.best_solution



    def __clean_population_for_duplicates_in_solution(self, population: List[SolutionGA]):
        for solution in population:
            unique_sets = set()
            for area in solution.population:
                mass_coordinate = (area.mass_coordinate['x'], area.mass_coordinate['z'])
                if mass_coordinate in unique_sets:
                    solution.population.remove(area)
                else:
                    unique_sets.add(mass_coordinate)
