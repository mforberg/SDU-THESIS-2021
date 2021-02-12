import random
from ..variables import *
import map_initial_population


class DistrictGA:

    def run(self, total_block_dict, total_surface_dict, district_areas):
        populations = []
        # Generate initial population
        for i in range(0, population_size-1):
            initial_population = map_initial_population.InitialPopulation().create(district_areas)
            populations.append({"population": initial_population, "fitness": None})

