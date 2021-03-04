import random
from variables.shared_variables import *
from variables.ga_type_variables import *


class TypeInitialPopulation:

    def create(self, clusters: SolutionGA) -> SolutionGA:
        list_of_area = []
        for cluster in clusters.population:
            area_type = self.get_random_type()
            coordinates = cluster.list_of_coordinates
            current_area = SolutionArea(coordinates=coordinates, type_of_district=area_type,
                                        min_max_values=cluster.min_max_values, height=-1,
                                        mass_coordinate=cluster.mass_coordinate)
            list_of_area.append(current_area)
        return SolutionGA(fitness=0, population=list_of_area)

    def get_random_type(self) -> str:
        random_index = random.randint(0, len(DISTRICT_TYPES) - 1)
        return DISTRICT_TYPES[random_index]
