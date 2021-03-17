from variables.map_variables import *
from a_star import AStar


class PrepareMap:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.a_star = AStar(surface_dict=surface_dict, fluid_set=fluid_set)

    def run(self, blocked_coordinates: set, connection_points: List[List[tuple]]) -> List[tuple]:
        return self.a_star.run(blocked_coordinates=blocked_coordinates, connection_points=connection_points)
