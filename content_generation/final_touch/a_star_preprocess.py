from wfc_variables import *


class AStarPreprocess:

    def run(self, cluster_list: List[Cluster], connection_tiles: List[tuple]) -> (set, List[tuple]):
        blocked_coordinates = set()
        connection_points = []
        for cluster in cluster_list:
            for tile in cluster.tiles:
                for coordinate in tile.nodes:
                    blocked_coordinates.add(coordinate)

        for connection_point in connection_tiles:
            first_list = []
            for node in connection_point[0].nodes:
                first_list.append(node)
                if node in blocked_coordinates:
                    blocked_coordinates.remove(node)
            second_list = []
            for node in connection_point[1].nodes:
                second_list.append(node)
                if node in blocked_coordinates:
                    blocked_coordinates.remove(node)
            connection_points.append((first_list, second_list))
        return blocked_coordinates, connection_points
