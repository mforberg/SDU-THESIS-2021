from typing import List

from variables.ga_type_variables import *
from .type_initial_population import TypeInitialPopulation
from .type_fitness import TypeFitness
from .type_selection import TypeSelection


class TypesGA:

    best_solution = None

    def run(self, surface_dict: dict, areas: List[List[tuple]]):

        population = []
        # Generate initial population
        for i in range(0, TYPE_POPULATION_SIZE):
            initial_population = TypeInitialPopulation().create(districts=areas)
            population.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in range(0, TYPE_GENERATION_AMOUNT):
            print(f"Current generation in Type_GA: {i}")
            TypeFitness().calculate_fitness_for_all(population=population)
            TypeSelection.select_best_solutions()

