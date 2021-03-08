from variables.ga_type_variables import *
from variables.shared_variables import *
from .type_preprocess import run_preprocess
from .type_initial_population import TypeInitialPopulation
from .type_fitness import TypeFitness
from .type_selection import TypeSelection
from .type_crossover import TypeCrossover
from .type_mutation import TypeMutation


class TypesGA:
    best_solution = SolutionGA(fitness=0, population=[SolutionArea(coordinates=[], mass_coordinate={},
                                                                   min_max_values={}, height=0,
                                                                   type_of_district="no")])

    def run(self, surface_dict: dict, clusters: SolutionGA, global_district_types_dict: dict,
            fluid_set: set) -> SolutionGA:
        preprocess_dict = run_preprocess(solution=clusters, surface_dict=surface_dict, fluid_set=fluid_set)
        population_list = []
        # Generate initial population
        for i in range(0, TYPE_POPULATION_SIZE):
            initial_population = TypeInitialPopulation().create(clusters=clusters)
            population_list.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in range(0, TYPE_GENERATION_AMOUNT):
            print(f"Current generation in Type_GA: {i}")
            TypeFitness().calculate_fitness_for_all(population_list=population_list, surface_dict=surface_dict,
                                                    global_dict_of_used_types=global_district_types_dict,
                                                    preprocess_dict=preprocess_dict)
            self.__check_for_new_best_solution(populations_list=population_list)
            # as long as it is not the last generation, find parents, do crossover, and mutate
            if i != TYPE_GENERATION_AMOUNT - 1:
                parents_no_fitness = TypeSelection().select_best_solutions(population_list=population_list)
                crossed_population_no_fitness = TypeCrossover().crossover(population_list, parents_no_fitness)
                TypeMutation().mutate_populations(crossed_population_no_fitness)
                population_list = crossed_population_no_fitness
        self.__update_global_dict_of_types(solution=self.best_solution,
                                           global_dict_of_used_types=global_district_types_dict)
        return self.best_solution

    def __update_global_dict_of_types(self, solution: SolutionGA, global_dict_of_used_types: dict):
        for area in solution.population:
            if area.type_of_district in global_dict_of_used_types:
                global_dict_of_used_types[area.type_of_district] += 1
            else:
                global_dict_of_used_types[area.type_of_district] = 1

    def __check_for_new_best_solution(self, populations_list):
        for solution in populations_list:
            if solution.fitness > self.best_solution.fitness:
                self.best_solution = copy.deepcopy(solution)
                print(f"New best {solution.fitness}")
