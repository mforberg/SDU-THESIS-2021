from typing import List

from variables.ga_type_variables import *
from .type_initial_population import TypeInitialPopulation
from .type_fitness import TypeFitness
from .type_selection import TypeSelection


class TypesGA:

    best_solution = {"solution": [{"population": None, "type": None}], "fitness": 0}

    def run(self, surface_dict: dict, areas: List[List[tuple]]):

        populations = []
        # Generate initial population
        for i in range(0, TYPE_POPULATION_SIZE):
            initial_population = TypeInitialPopulation().create(areas=areas)
            populations.append(initial_population)
        # repeat fitness calculation and select the best solution overall
        for i in range(0, TYPE_GENERATION_AMOUNT):
            print(f"Current generation in Type_GA: {i}")
            TypeFitness().calculate_fitness_for_all(populations=populations)

