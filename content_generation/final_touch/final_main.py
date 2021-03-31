from a_star import AStar
from a_star_preprocess import AStarPreprocess
from wfc_variables import *


class PrepareMap:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.a_star = AStar(surface_dict=surface_dict, fluid_set=fluid_set)

    def run(self, cluster_list: List[Cluster], connection_tiles: List[tuple]) -> List[tuple]:
        blocked_coordinates, connection_points = AStarPreprocess().run(cluster_list=cluster_list,
                                                                       connection_tiles=connection_tiles)

        return self.a_star.run(blocked_coordinates=blocked_coordinates, connection_points=connection_points)
