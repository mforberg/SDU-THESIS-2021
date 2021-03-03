from variables.ga_type_variables import *
from map_shared_variables import *
from .type_initial_population import TypeInitialPopulation
from .type_fitness import TypeFitness
from .type_selection import TypeSelection
from .type_crossover import TypeCrossover
from .type_mutation import TypeMutation


class TypesGA:
    dummy_solution = SolutionType(fitness=0, population=[AreaType(area_type="None", coordinates=[])], amount=0)
    best_solution = dummy_solution

    def run(self, surface_dict: dict, clusters: List[List[list]]) -> SolutionType:
        population_list = []
        # Generate initial population
        for i in range(0, TYPE_POPULATION_SIZE):
            initial_population = TypeInitialPopulation().create(clusters=clusters)
            population_list.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in range(0, TYPE_GENERATION_AMOUNT):
            print(f"Current generation in Type_GA: {i}")
            TypeFitness().calculate_fitness_for_all(population_list=population_list)
            self.check_for_new_best_solution(populations_list=population_list)
            # as long as it is not the last generation, find parents, do crossover, and mutate
            if i != TYPE_GENERATION_AMOUNT - 1:
                parents_no_fitness = TypeSelection().select_best_solutions(population_list=population_list)
                crossed_population_no_fitness = TypeCrossover().crossover(population_list, parents_no_fitness)
                TypeMutation().mutate_populations(crossed_population_no_fitness)
                population_list = crossed_population_no_fitness
        return self.best_solution

    def check_for_new_best_solution(self, populations_list):
        for solution in populations_list:
            if solution.fitness > self.best_solution.fitness:
                self.best_solution = copy.deepcopy(solution)
                print(f"New best {solution.fitness}")
