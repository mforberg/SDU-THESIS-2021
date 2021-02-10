import random
import map_initial_population


class DistrictGA:

    def run(self, total_block_dict, total_surface_dict, district_areas):
        initial_population = map_initial_population.InitialPopulation().create()
