from wfc_tile import *
import math


class ConnectionPoints:

    def __init__(self, clusters: list):
        self.clusters = clusters
        self.connection_points = []
        self.connected_clusters = []
        self.total_connected_list = []

    def run(self):
        self.__find_connection_tiles_next_to_each_other()
        self.__connect_everything()

    def __connect_everything(self):
        self.total_connected_list.append(self.clusters[0])
        while len(self.total_connected_list) < len(self.clusters):
            to_be_added = []
            for cluster in self.total_connected_list:
                connected_clusters = self.__get_clusters_connected_to_this(cluster=cluster)
                if len(connected_clusters) > 0:
                    to_be_added.extend(connected_clusters)
                else:
                    self.__find_nearest_connection_point(cluster=cluster)
            for cluster in to_be_added:
                if cluster not in self.total_connected_list:
                    self.total_connected_list.append(cluster)

    def __find_nearest_connection_point(self, cluster):
        shortest_distance = 9999999999999999999999999999
        connection_point = None
        from_cluster = None
        for other_cluster in self.clusters:
            if cluster != other_cluster:
                for tile in cluster:
                    closest_tile, tile_distance = self.__find_nearest_tile(tile=tile, other_cluster=other_cluster)
                    if tile_distance < shortest_distance:
                        shortest_distance = tile_distance
                        connection_point = (tile, closest_tile)
                        from_cluster = other_cluster
        self.connection_points.append(connection_point)
        self.connected_clusters.append((cluster, from_cluster))

    def __find_nearest_tile(self, tile, other_cluster):
        final_tile = tile
        shortest_distance = 9999999999999999999999999999

        total_z = 0
        total_x = 0
        for node in tile.nodes:
            total_x += node[0]
            total_z += node[1]
        center_x = total_x / len(tile.nodes)
        center_z = total_z / len(tile.nodes)

        for other_tile in other_cluster:
            other_total_z = 0
            other_total_x = 0
            for node in other_tile.nodes:
                other_total_x += node[0]
                other_total_z += node[1]
            other_center_x = total_x / len(other_tile.nodes)
            other_center_z = total_z / len(other_tile.nodes)
            distance = math.sqrt(math.pow(center_x - other_center_x, 2) + math.pow(center_z - other_center_z, 2))
            if distance < shortest_distance:
                shortest_distance = distance
                final_tile = other_tile
        return final_tile, shortest_distance

    def __get_clusters_connected_to_this(self, cluster) -> list:
        connected_clusters = []
        for connection in self.connected_clusters:
            if connection[0] == cluster:
                connected_clusters.append(connection[1])
            elif connection[1] == cluster:
                connected_clusters.append(connection[0])
        return connected_clusters

    def __find_connection_tiles_next_to_each_other(self):
        skip_clusters = set()
        for cluster in self.clusters:
            skip_clusters.add(cluster)
            for tile in cluster:
                for other_cluster in self.clusters:
                    if other_cluster not in skip_clusters:
                        neighbors = self.__find_neighbors_in_cluster(tile=tile, other_cluster=other_cluster)
                        for neighbor in neighbors:
                            self.connection_points.append((tile, neighbor))
                            self.connected_clusters.append((cluster, other_cluster))

    def __find_neighbors_in_cluster(self, tile, other_cluster) -> List[Tile]:
        list_of_neighbors_in_other_clusters = []
        for neighbor in tile.neighbors:
            if neighbor in other_cluster:
                list_of_neighbors_in_other_clusters.append(neighbor)
        return list_of_neighbors_in_other_clusters
