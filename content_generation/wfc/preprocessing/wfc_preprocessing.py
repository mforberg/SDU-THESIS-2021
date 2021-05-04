import time
from typing import List
from shared_models import SolutionGA, SurfaceDictionaryValue
from wfc_models import Tile, Cluster
from pprint import pprint
from copy import deepcopy
from collections import Counter
import numpy

class WFCPreprocessing:

    def __init__(self):
        # this is needed to draw grid over the whole solution so that it can be divided into tiles
        self.__min_x, self.__min_z = 9999999, 9999999 #numpy.inf, numpy.inf
        self.__max_x, self.__max_z = -9999999, -9999999 #-numpy.inf, -numpy.inf
        self.n = 2  # just a default value

    def create_tiles(self, result: SolutionGA, tile_size: int, surface_dict: dict):
        # TODO: Remove print statements when code is functional
        n = tile_size
        self.n = tile_size

        # Set min/max x/z values of all coordinates in full solution
        self.__set_min_max_values(self.__get_min_max_values(result))
        self.__print_modulo_n(n)

        # Prune edges if delta_x or delta_z mod n is not 0; delta z/x has to be a rectangle dividable by n
        print(f"(FIRST) max_x: {self.__max_x} min_x: {self.__min_x} max_z: {self.__max_z} min_z: {self.__min_z}")
        self.__prune_edges(n, result)
        self.__set_min_max_values(self.__get_min_max_values(result))
        self.__print_modulo_n(n)

        # Create tileset for solution
        total_coordinates = []
        for solution in result.population:
            total_coordinates.extend(solution.list_of_coordinates)
        total_set_coordinates = set(total_coordinates)

        solution_tiles = self.__generate_tileset(n, total_set_coordinates)

        # Assign tiles to cluster
        clustered_tiles = self.__clustered_tileset(solution_tiles, result)

        print(((self.__max_x - self.__min_x) / n) * ((self.__max_z - self.__min_z) / n))
        print(f"N={n}, max_x-min_x={self.__max_x - self.__min_x}, delta_x%n={(self.__max_x - self.__min_x + 1) % n}")
        print(f"(SECOND) max_x: {self.__max_x} min_x: {self.__min_x} max_z: {self.__max_z} min_z: {self.__min_z}")

        return solution_tiles, clustered_tiles

    def remove_neighbors(self, clustered_tiles: List[Cluster]):
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                for neighbor in tile.neighbors:
                    if tile.cluster_assignment != neighbor.cluster_assignment:
                        tile.remove_neighbor(neighbor)

    def __clustered_tileset(self, solution_tiles, result):
        cluster_list_with_neighbors = [Cluster([]) for _ in range(len(result.population))]
        coordinate_cluster_dict = {}
        coordinate_cluster_list = []
        build_list = []

        # Create dictionary with x, z = cluster_assignment
        for i in range(len(result.population)):
            temp = set()
            for coord in result.population[i].list_of_coordinates:
                coordinate_cluster_dict[coord] = i
                temp.add(coord)
            coordinate_cluster_list.append(temp)

        # Assign tiles to their specific clusters, with all neighbors intact
        for tile in solution_tiles:
            counter_dict = {n: 0 for n in range(len(coordinate_cluster_list))}

            for coord in tile.nodes:
                for i in range(len(coordinate_cluster_list)):
                    if coord in coordinate_cluster_list[i]:
                        counter_dict[i] += 1
            if sum(counter_dict.values()) < (self.n * self.n):
                build_list.append(tile)
            max_key = max(counter_dict, key=counter_dict.get)
            tile.cluster_assignment = max_key
            cluster_list_with_neighbors[max_key].tiles.append(tile)

        return build_list, cluster_list_with_neighbors

    def normalize_height(self, clustered_tiles, surface_dict):
        for cluster in clustered_tiles:
            test = {}
            for tile in cluster.tiles:
                for node in tile.nodes:
                    value: SurfaceDictionaryValue = surface_dict[node]
                    if value.y not in test:
                        test[value.y] = 0
                    else:
                        test[value.y] += 1
            max_key = max(test, key=test.get)
            cluster.y = max_key


    def __generate_tileset(self, n, coordinates):
        solution_tiles = []
        existing_nodes = {}

        # -n: Subtract to not go out of bounds, as the LAST tiles in a row/column will be at max_x - n
        # +2: +1 because range is not inclusive, and also +1 to ensure last row of tiles is created
        for x in range(self.__min_x, (self.__max_x - n) + 2, n):
            for z in range(self.__min_z, (self.__max_z - n) + 2, n):

                # Create NxN nodes
                nodes = []
                for x_range_n in range(0, n):
                    for z_range_n in range(0, n):
                        x1 = x + x_range_n
                        z1 = z + z_range_n
                        nodes.append((x1, z1))

                tile = Tile(nodes)

                # Add tile if any node is part of solution space
                if set(nodes).intersection(coordinates):
                    existing_nodes[x, z] = tile
                    solution_tiles.append(tile)

                # Add neighbors to tiles
                neighbor_directions = [(0, 3), (0, -3), (3, 0), (-3, 0)]
                for direction in neighbor_directions:
                    neighbor_x = x + direction[0]
                    neighbor_z = z + direction[1]

                    if (neighbor_x, neighbor_z) in existing_nodes:
                        tile.add_neighbor(existing_nodes[neighbor_x, neighbor_z])

        return solution_tiles

    def __prune_edges(self, n: int, result: SolutionGA):
        dicts = []
        delta_x_mod_n = (self.__max_x - self.__min_x + 1) % n
        delta_z_mod_n = (self.__max_z - self.__min_z + 1) % n
        while delta_x_mod_n != 0:
            edge_nodes = self.__find_edge_node_count(result)
            dicts.append(self.__prune_single_edge(edge_nodes, n, result, self.__min_x, self.__max_x, 'x'))
            self.__set_min_max_values(self.__get_min_max_values(result))
            delta_x_mod_n -= 1
        while delta_z_mod_n != 0:
            edge_nodes = self.__find_edge_node_count(result)
            dicts.append(self.__prune_single_edge(edge_nodes, n, result, self.__min_z, self.__max_z, 'z'))
            self.__set_min_max_values(self.__get_min_max_values(result))
            delta_z_mod_n -= 1
        self.__set_min_max_values(self.__get_min_max_values(result))
        delete_counter = {'min_x': 0, 'max_x': 0, 'min_z': 0, 'max_z': 0}

        for d in dicts:
            for key in d:
                value = d[key]
                delete_counter[key] += value
        print(f"deleted nodes: {delete_counter}")

    def __prune_single_edge(self, edge_nodes, n, result, min_value, max_value, edge: str) -> dict:
        deleted_edge = max_value
        count_min, count_max = 0, 0

        for item in edge_nodes:
            count_min += item[min_value]
            count_max += item[max_value]

        if count_max > count_min:
            deleted_edge = min_value

        count = 0
        for pop in result.population:
            for coord in reversed(pop.list_of_coordinates):
                if edge == 'x':
                    if coord[0] == deleted_edge:
                        count += 1
                        pop.list_of_coordinates.remove(coord)
                if edge == 'z':
                    if coord[1] == deleted_edge:
                        count += 1
                        pop.list_of_coordinates.remove(coord)

        delete_counter = {'min_x': 0, 'max_x': 0, 'min_z': 0, 'max_z': 0}
        if edge == 'x':
            if deleted_edge == min_value:
                delete_counter['min_x'] += count
            else:
                delete_counter['max_x'] += count
        elif edge == 'z':
            if deleted_edge == min_value:
                delete_counter['min_z'] += count
            else:
                delete_counter['max_z'] += count
        return delete_counter

    def __print_modulo_n(self, n):
        print(f"width (X):{self.__max_x - self.__min_x}, height (Z): {self.__max_z - self.__min_z}")
        print(f"(N={n}) X%N: {(self.__max_x - self.__min_x) % n}, Z%N: {(self.__max_z - self.__min_z) % n}")

    def __find_edge_node_count(self, result: SolutionGA) -> List[dict]:
        counters = []
        for solution_area in result.population:
            temp = {self.__min_x: 0, self.__max_x: 0, self.__min_z: 0, self.__max_z: 0}
            for coordinate in solution_area.list_of_coordinates:
                # (x, y)
                if coordinate[0] == self.__max_x:
                    temp[self.__max_x] += 1
                if coordinate[0] == self.__min_x:
                    temp[self.__min_x] += 1
                if coordinate[1] == self.__max_z:
                    temp[self.__max_z] += 1
                if coordinate[1] == self.__min_z:
                    temp[self.__min_z] += 1
            counters.append(temp)
        return counters

    def __set_min_max_values(self, values: (int, int, int, int)):
        self.__max_x = values[0]
        self.__max_z = values[1]
        self.__min_x = values[2]
        self.__min_z = values[3]

    def __get_min_max_values(self, result: SolutionGA) -> (int, int, int, int):
        min_x, min_z = 9999999, 9999999 #self.__min_x, self.__min_z
        max_x, max_z = -9999999, -9999999 #self.__max_x, self.__max_z
        for population in result.population:
            population.recalculate_min_max_mass()
            min_max_dict = population.min_max_values
            max_x, max_z, min_x, min_z = self.__compare_min_max_values(min_max_dict, max_x, max_z, min_x, min_z)
        return max_x, max_z, min_x, min_z

    # noinspection PyMethodMayBeStatic
    def __compare_min_max_values(self, min_max_dict, max_x, max_z, min_x, min_z) -> (int, int, int, int):
        if min_max_dict['min_x'] < min_x:
            min_x = min_max_dict['min_x']
        if min_max_dict['max_x'] > max_x:
            max_x = min_max_dict['max_x']
        if min_max_dict['min_z'] < min_z:
            min_z = min_max_dict['min_z']
        if min_max_dict['max_z'] > max_z:
            max_z = min_max_dict['max_z']
        return max_x, max_z, min_x, min_z
