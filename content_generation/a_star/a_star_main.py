from typing import List, Set
from a_star_algorithm import AStar
from a_star_models import APoint
from a_star_preprocess import AStarPreprocess
from wfc_models import Cluster


class AStarMain:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.a_star_preprocess = AStarPreprocess(surface_dict=surface_dict)
        self.a_star = AStar(surface_dict=surface_dict, fluid_set=fluid_set)

    def run(self, cluster_list: List[Cluster], connection_tiles: List[tuple]) -> List[tuple]:
        # self.__unit_test()
        blocked_coordinates, connection_points = self.a_star_preprocess.run(cluster_list=cluster_list,
                                                                            connection_tiles=connection_tiles)
        a_points = self.a_star.run(blocked_coordinates=blocked_coordinates, connection_points=connection_points)
        return self.__make_a_points_into_x_z_y(a_points=a_points)

    def __make_a_points_into_x_z_y(self, a_points: List[APoint]) -> List[tuple]:
        point_list = []
        for a_point in a_points:
            x = a_point.node[0]
            z = a_point.node[1]
            y = a_point.y
            point_list.append((x, z, y))
        return point_list

    def __unit_test(self):
        first = APoint(node=(0, 0), y=-1)
        second = APoint(node=(0, 0), y=2)
        print(f"Equal test: {first == second}")

        blocked_coordinates = set()
        test_point0 = APoint(node=(0, 0), y=1)
        blocked_coordinates.add(test_point0)

        test_point1 = APoint(node=(0, 0), y=75)
        test_point2 = APoint(node=(0, 0), y=-1)
        print(f"First 'in' test: {test_point0 in blocked_coordinates}")
        print(f"Second 'in' test: {test_point1 not in blocked_coordinates}")
        print(f"Third 'in' test: {test_point2 in blocked_coordinates}")
