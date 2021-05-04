from shared_models import SolutionGA


class MapAnalData:
    def __init__(self, block_dict: dict, surface_dict: dict, areas_for_districts: SolutionGA,
                 set_of_fluid_coordinates: set):
        self.block_dict = block_dict
        self.surface_dict = surface_dict
        self.areas_for_districts = areas_for_districts
        self.set_of_fluid_coordinates = set_of_fluid_coordinates
