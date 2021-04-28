from wfc_variables import *
import math


class ConnectionPoints:

    def __init__(self, clusters: List[Cluster]):
        self.clusters = clusters
        self.connection_points = []
        self.connected_clusters = []
        self.total_connected_list = []

    def run(self) -> List[tuple]:
        self.__find_connection_tiles_next_to_each_other()
        self.__connect_everything()
        # self.__connect_own_clusters()
        return self.connection_points

    def __connect_own_clusters(self):
        for cluster in self.clusters:
            connected_areas = []
            tile_iterator = iter(cluster.tiles)
            checked_tiles = set()
            while len(checked_tiles) < len(cluster.tiles):
                current_tile = next(tile_iterator)
                if current_tile not in checked_tiles:
                    connected_areas.append(self.__get_area_connected_to_this(cluster=cluster, tile=current_tile,
                                                                             checked_tiles=checked_tiles))
            own_cluster = [connected_areas[0]]
            i = 0
            while len(own_cluster) < len(connected_areas):
                closest = None
                connection_point = None
                shortest_distance = 9999999999999
                for inner_cluster in connected_areas:
                    if inner_cluster in own_cluster:
                        continue
                    result = self.__find_nearest_connection_point(cluster=inner_cluster, from_clusters=own_cluster)
                    temp_connection_point = result[0]
                    temp_distance = result[2]
                    if temp_distance < shortest_distance:
                        shortest_distance = temp_distance
                        connection_point = temp_connection_point
                        closest = inner_cluster
                self.connection_points.append(connection_point)
                own_cluster.append(closest)

    def __get_area_connected_to_this(self, tile: Tile, cluster: Cluster, checked_tiles: set) -> Cluster:
        tiles_to_be_checked = [tile]
        current_area = []
        cluster_tiles_set = set()
        for tile in cluster.tiles:
            cluster_tiles_set.add(tile)
        while tiles_to_be_checked:
            current_tile = tiles_to_be_checked.pop(0)
            checked_tiles.add(current_tile)
            current_area.append(current_tile)
            for neighbor in current_tile.neighbors:
                if neighbor not in checked_tiles and neighbor in cluster_tiles_set:
                    tiles_to_be_checked.append(neighbor)
        return Cluster(current_area)

    def __connect_everything(self):
        self.total_connected_list.append(self.clusters[0].id)
        new = True
        while len(self.total_connected_list) < len(self.clusters):
            to_be_added = []
            for cluster_id in self.total_connected_list:
                connected_clusters_ids = self.__get_clusters_connected_to_this(cluster_id=cluster_id)
                if len(connected_clusters_ids) > 0:
                    to_be_added.extend(connected_clusters_ids)
                else:
                    cluster = self.__get_cluster_from_id(cluster_id=cluster_id)
                    other_clusters = self.__get_all_clusters_not_connected()
                    result = self.__find_nearest_connection_point(cluster=cluster, from_clusters=other_clusters)
                    connection_point = result[0]
                    to_cluster = result[1]
                    self.connection_points.append(connection_point)
                    self.connected_clusters.append((cluster.id, to_cluster.id))
                    to_be_added.append(to_cluster.id)
            if not new:
                result = self.__connect_main_cluster_to_other_district()
                own_cluster = result[0]
                connection_point = result[1]
                to_cluster = result[2]
                self.connection_points.append(connection_point)
                self.connected_clusters.append((own_cluster.id, to_cluster.id))
                to_be_added.append(to_cluster.id)
            new = False
            for cluster_id in to_be_added:
                if cluster_id not in self.total_connected_list:
                    new = True
                    self.total_connected_list.append(cluster_id)

    def __connect_main_cluster_to_other_district(self) -> (Cluster, tuple, Cluster):
        other_clusters = self.__get_all_clusters_not_connected()
        total_shortest_distance = 999999999999999999
        own_cluster = None
        closest_cluster = None
        connection_point = None
        for cluster_id in self.total_connected_list:
            cluster = self.__get_cluster_from_id(cluster_id=cluster_id)
            result = self.__find_nearest_connection_point(cluster=cluster, from_clusters=other_clusters)
            shortest_distance = result[2]
            if shortest_distance < total_shortest_distance:
                own_cluster = cluster
                total_shortest_distance = shortest_distance
                closest_cluster = result[1]
                connection_point = result[0]
        return own_cluster, connection_point, closest_cluster

    def __find_nearest_connection_point(self, cluster: Cluster, from_clusters: List[Cluster]) -> (tuple, Cluster, int):
        shortest_distance = 9999999999999999999999999999
        connection_point = None
        to_cluster = None
        for other_cluster in from_clusters:
            if cluster != other_cluster:
                for tile in cluster.tiles:
                    closest_tile, tile_distance = self.__find_nearest_tile(tile=tile, other_cluster=other_cluster)
                    if tile_distance < shortest_distance:
                        shortest_distance = tile_distance
                        connection_point = (tile, closest_tile)
                        to_cluster = other_cluster
        return connection_point, to_cluster, shortest_distance

    def __get_all_clusters_not_connected(self) -> List[Cluster]:
        not_connected = []
        for cluster in self.clusters:
            if cluster.id not in self.total_connected_list:
                not_connected.append(cluster)
        return not_connected

    def __find_nearest_tile(self, tile: Tile, other_cluster: Cluster):
        final_tile = tile
        shortest_distance = 9999999999999999999999999999

        total_z = 0
        total_x = 0
        for node in tile.nodes:
            total_x += node[0]
            total_z += node[1]
        center_x = total_x / len(tile.nodes)
        center_z = total_z / len(tile.nodes)

        for other_tile in other_cluster.tiles:
            other_total_z = 0
            other_total_x = 0
            for node in other_tile.nodes:
                other_total_x += node[0]
                other_total_z += node[1]
            other_center_x = other_total_x / len(other_tile.nodes)
            other_center_z = other_total_z / len(other_tile.nodes)
            distance = math.sqrt(math.pow(center_x - other_center_x, 2) + math.pow(center_z - other_center_z, 2))
            if distance < shortest_distance:
                shortest_distance = distance
                final_tile = other_tile
        return final_tile, shortest_distance

    def __get_clusters_connected_to_this(self, cluster_id: str) -> List[str]:
        connected_clusters = []
        for connection_ids in self.connected_clusters:
            first_cluster = self.__get_cluster_from_id(connection_ids[0])
            second_cluster = self.__get_cluster_from_id(connection_ids[1])
            if first_cluster.id == cluster_id:
                connected_clusters.append(connection_ids[1])
            elif second_cluster.id == cluster_id:
                connected_clusters.append(connection_ids[0])
        return connected_clusters

    def __get_cluster_from_id(self, cluster_id):
        for cluster in self.clusters:
            if cluster.id == cluster_id:
                return cluster

    def __find_connection_tiles_next_to_each_other(self):
        connection_dict = {}
        skip_clusters = set()
        for cluster in self.clusters:
            skip_clusters.add(cluster)
            for tile in cluster.tiles:
                for other_cluster in self.clusters:
                    if other_cluster not in skip_clusters:
                        neighbors = self.__find_neighbors_in_cluster(tile=tile, other_cluster=other_cluster)
                        for neighbor in neighbors:
                            if (cluster.id, other_cluster.id) in connection_dict:
                                connection_dict[(cluster.id, other_cluster.id)].append((tile, neighbor))
                            else:
                                connection_dict[(cluster.id, other_cluster.id)] = [(tile, neighbor)]
        self.__find_single_connection_point_for_each_linked_connection(connection_dict=connection_dict)

    def __find_single_connection_point_for_each_linked_connection(self, connection_dict: dict):
        skip_tuple = set()
        for cluster_ids, list_of_tiles_connected in connection_dict.items():
            for tup in list_of_tiles_connected:
                if tup in skip_tuple:
                    continue
                connected = [tup]
                check_tup = [tup]
                skip_tuple.add(tup)
                while check_tup:
                    current_tile_tuple = check_tup.pop(0)
                    result = self.__get_all_connected_to_this_tile(tile_tuple=current_tile_tuple, skip_tuple=skip_tuple,
                                                                   list_of_tiles_connected=list_of_tiles_connected)
                    for connected_tup in result:
                        connected.append(connected_tup)
                        check_tup.append(connected_tup)
                self.__add_middle_point_to_connection_points(list_of_tuples_containing_tiles=connected)
            self.connected_clusters.append(cluster_ids)

    def __add_middle_point_to_connection_points(self, list_of_tuples_containing_tiles: List[tuple]):
        total_x = total_z = 0
        amount = 0
        for tup_of_tiles in list_of_tuples_containing_tiles:
            for node in tup_of_tiles[0].nodes:
                amount += 1
                total_x += node[0]
                total_z += node[1]
        avg_x = total_x / amount
        avg_z = total_z / amount
        closest_tiles_tuple = None
        shortest_distance = 999999999999999999999
        for tup_of_tiles in list_of_tuples_containing_tiles:
            node_x = 0
            node_z = 0
            for node in tup_of_tiles[0].nodes:
                node_x += node[0]
                node_z += node[1]
            node_x /= len(tup_of_tiles[0].nodes)
            node_z /= len(tup_of_tiles[0].nodes)
            distance = math.sqrt(math.pow(node_x - avg_x, 2) + math.pow(node_z - avg_z, 2))
            if distance < shortest_distance:
                shortest_distance = distance
                closest_tiles_tuple = tup_of_tiles
        self.connection_points.append(closest_tiles_tuple)

    def __get_all_connected_to_this_tile(self, tile_tuple: tuple, skip_tuple: set,
                                         list_of_tiles_connected: List[tuple]) -> List[tuple]:
        list_of_neighbors_connected = []
        for neighbor in tile_tuple[0].neighbors:
            for tup in list_of_tiles_connected:
                if tup in skip_tuple:
                    continue
                if neighbor == tup[0]:
                    list_of_neighbors_connected.append(tup)
                    skip_tuple.add(tup)
            for neighbor_neighbor in neighbor.neighbors:
                for tup in list_of_tiles_connected:
                    if tup in skip_tuple:
                        continue
                    if neighbor_neighbor == tup[0]:
                        list_of_neighbors_connected.append(tup)
                        skip_tuple.add(tup)
        return list_of_neighbors_connected

    def __find_neighbors_in_cluster(self, tile: Tile, other_cluster: Cluster) -> List[Tile]:
        list_of_neighbors_in_other_clusters = []
        for neighbor in tile.neighbors:
            if neighbor in other_cluster.tiles:
                list_of_neighbors_in_other_clusters.append(neighbor)
        return list_of_neighbors_in_other_clusters
