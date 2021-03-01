import random
from variables.shared_variables import *
from variables.ga_type_variables import *


class TypeInitialPopulation:

    def create(self, districts: SolutionGA) -> SolutionGA:
        list_of_area = []
        for district in districts.population:
            area_type = self.get_random_type()

            current_area = AreaMap(area_type=area_type, area_set=district.area_set, height=district.height,
                                   coordinates=district.list_of_coordinates, mass_coordinate=district.mass_coordinate,
                                   min_max_values=district.min_max_values)
            list_of_area.append(current_area)
        return SolutionGA(fitness=0, population=list_of_area, amount=1)

    def get_random_type(self) -> str:
        random_index = random.randint(0, len(DISTRICT_TYPES) - 1)
        return DISTRICT_TYPES[random_index]
