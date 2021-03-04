import random
from variables.shared_variables import *
from variables.ga_type_variables import *


class TypeInitialPopulation:

    def create(self, clusters: List[List[list]]) -> SolutionGA:
        list_of_area = []
        for cluster in clusters:
            area_type = self.get_random_type()
            coordinates = self.convert_list_of_list_to_list_of_tuples(cluster=cluster)
            current_area = SolutionArea(coordinates=coordinates, type_of_district=area_type,
                                        min_max_values={"no": True}, height=-1, mass_coordinate={"no": True})
            list_of_area.append(current_area)
        return SolutionGA(fitness=0, population=list_of_area)

    def get_random_type(self) -> str:
        random_index = random.randint(0, len(DISTRICT_TYPES) - 1)
        return DISTRICT_TYPES[random_index]

    def convert_list_of_list_to_list_of_tuples(self, cluster: List[list]) -> List[tuple]:
        new_list = []
        for coordinate in cluster:
            new_list.append((coordinate[0], coordinate[1]))
        return new_list
