from typing import List

import shared_models


class PreProcessData:

    def __init__(self, water_list: List[tuple], resource_list: List[tuple]):
        self.water_list = water_list
        self.resource_list = resource_list
        self.water_mass = shared_models.calculate_mass_coordinate(water_list)
        self.resource_mass = shared_models.calculate_mass_coordinate(resource_list)
