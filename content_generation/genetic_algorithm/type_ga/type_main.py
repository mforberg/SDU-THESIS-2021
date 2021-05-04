from ga_specific_models import DataFileCreator
from selection import Selection
from variables.ga_type_variables import *
from type_preprocess import run_preprocess
from type_initial_population import TypeInitialPopulation
from type_fitness import TypeFitness
from type_crossover import TypeCrossover
from type_mutation import TypeMutation
from shared_models import *
from tqdm import trange


class TypesGA:

    def __init__(self):
        self.best_solution = SolutionGA(fitness=0, population=[SolutionArea(coordinates=[], mass_coordinate={},
                                                                            min_max_values={}, height=0,
                                                                            type_of_district="no")])
        self.DFC = DataFileCreator(filename="type_ga_data")
        self.new_best_prints = []
        self.type_initial = TypeInitialPopulation()
        self.type_fitness = TypeFitness()
        self.type_select = Selection(TYPE_AMOUNT_OF_PARENTS_CHOSEN)
        self.type_crossover = TypeCrossover(TYPE_POPULATION_SIZE)
        self.type_mutation = TypeMutation()

    def run(self, surface_dict: dict, clusters: SolutionGA, global_district_types_dict: dict,
            fluid_set: set) -> SolutionGA:
        preprocess_dict = run_preprocess(solution=clusters, surface_dict=surface_dict, fluid_set=fluid_set)
        population = []
        # Generate initial population
        for i in range(0, TYPE_POPULATION_SIZE):
            initial_population = self.type_initial.create(clusters=clusters)
            population.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in trange(TYPE_GENERATION_AMOUNT, desc='GA for setting type', leave=True):
            self.type_fitness.calculate_fitness_for_all(population_list=population, surface_dict=surface_dict,
                                                        global_dict_of_used_types=global_district_types_dict,
                                                        preprocess_dict=preprocess_dict)
            r = self.DFC.check_stats_on_solution(population=population, current_gen=i, best_solution=self.best_solution)
            self.new_best_prints.extend(r[0])
            self.best_solution = r[1]
            # as long as it is not the last generation, find parents, do crossover, and mutate
            if i != TYPE_GENERATION_AMOUNT - 1:
                parents_no_fitness = self.type_select.select_best_solutions(population_list=population)
                crossed_population_no_fitness = self.type_crossover.crossover(population, parents_no_fitness)
                self.type_mutation.mutate_populations(crossed_population_no_fitness)
                population = crossed_population_no_fitness
        self.__update_global_dict_of_types(solution=self.best_solution,
                                           global_dict_of_used_types=global_district_types_dict)
        # for string in self.new_best_prints:
        #     print(string)
        return self.best_solution

    def __update_global_dict_of_types(self, solution: SolutionGA, global_dict_of_used_types: dict):
        for area in solution.population:
            if area.type_of_district in global_dict_of_used_types:
                global_dict_of_used_types[area.type_of_district] += 1
            else:
                global_dict_of_used_types[area.type_of_district] = 1
    #
    # def __check_for_new_best_solution(self, populations_list: list, current_gen: int):
    #     for solution in populations_list:
    #         if solution.fitness > self.best_solution.fitness:
    #             self.best_solution = copy.deepcopy(solution)
    #             self.new_best_prints.append(f"New best {solution.fitness} at gen {current_gen}")
