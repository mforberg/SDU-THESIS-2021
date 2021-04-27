from typing import Set

from wfc_variables import *
from a_star_variables import *


class AStarPreprocess:

    def __init__(self, surface_dict: dict):
        self.surface_dict = surface_dict

    def run(self, cluster_list: List[Cluster], connection_tiles: List[tuple]) -> (Set[APoint], List[tuple]):
        blocked_coordinates = set()
        connection_points = []
        for cluster in cluster_list:
            for tile in cluster.tiles:
                for coordinate in tile.nodes:
                    blocked_coordinates.add(APoint(node=coordinate, y=-1))

        for connection_point in connection_tiles:
            first_list = []
            for node in connection_point[0].nodes:
                y = self.surface_dict[node].y
                point = APoint(node=node, y=y)
                first_list.append(point)
                if point in blocked_coordinates:
                    blocked_coordinates.remove(point)
            second_list = []
            for node in connection_point[1].nodes:
                y = self.surface_dict[node].y
                point = APoint(node=node, y=y)
                second_list.append(point)
                if point in blocked_coordinates:
                    blocked_coordinates.remove(point)
            connection_points.append((first_list, second_list))
        return blocked_coordinates, connection_points
