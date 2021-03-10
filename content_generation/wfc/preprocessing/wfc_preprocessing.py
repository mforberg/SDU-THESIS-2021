import time
from typing import List
from shared_variables import SolutionGA


class WFCPreprocessing:

    def __init__(self):
        # this is needed to draw grid over the whole solution so that it can be divided into tiles
        self.min_x, self.min_z = 9999999, 9999999
        self.max_x, self.max_z = -9999999, -9999999

    def create_tiles(self, result: SolutionGA, tile_size: int):

        n = tile_size

        self.__set_min_max_values(self.__get_min_max_values(result))
        self.__print_modulo_n(n)

        # TODO: If you check min / max x / z, and you know the edge with most duplicates (e.g. max_x)
        #  you can find direction by adding / subtracting 1 to x by looking at opposite value (e.g. min_X)

        print(f"max_x: {self.max_x} min_x: {self.min_x} max_z: {self.max_z} min_z: {self.min_z}")
        self.__prune_edges(n, result)

        self.__set_min_max_values(self.__get_min_max_values(result))
        self.__print_modulo_n(n)

    def __prune_edges(self, n: int, result: SolutionGA):
        dicts = []
        while (self.max_x - self.min_x) % n != 0:
            edge_nodes = self.__find_edge_node_count(result)
            dicts.append(self.__prune_single_edge(edge_nodes, n, result, self.min_x, self.max_x, 'x'))
            self.__set_min_max_values(self.__get_min_max_values(result))
        while (self.max_z - self.min_z) % n != 0:
            edge_nodes = self.__find_edge_node_count(result)
            dicts.append(self.__prune_single_edge(edge_nodes, n, result, self.min_z, self.max_z, 'z'))
            self.__set_min_max_values(self.__get_min_max_values(result))
        delete_counter = {'min_x': 0, 'max_x': 0, 'min_z': 0, 'max_z': 0}
        for d in dicts:
            for key in d:
                value = d[key]
                delete_counter[key] += value
        result.update_sets()
        print(delete_counter)

    def __prune_single_edge(self, edge_nodes, n, result, min_value, max_value, edge: str) -> dict:
        if (max_value - min_value) % n != 0:
            print(f"edge is broken {(max_value - min_value) % n} (N={n})")
            deleted_edge = max_value
            count_min, count_max = 0, 0

            for item in edge_nodes:
                count_min += item[min_value]
                count_max += item[max_value]

            if count_max > count_min:
                deleted_edge = min_value

            print(f"{count_max} > {count_min}?")
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
        print(f"width (X):{self.max_x - self.min_x}, height (Z): {self.max_z - self.min_z}")
        print(f"(N={n}) X%N: {(self.max_x - self.min_x) % n}, Z%N: {(self.max_z - self.min_z) % n}")

    def __find_edge_node_count(self, result: SolutionGA) -> List[dict]:
        counters = []
        for solution_area in result.population:
            temp = {self.min_x: 0, self.max_x: 0, self.min_z: 0, self.max_z: 0}
            for coordinate in solution_area.list_of_coordinates:
                # (x, y)
                if coordinate[0] == self.max_x:
                    temp[self.max_x] += 1
                if coordinate[0] == self.min_x:
                    temp[self.min_x] += 1
                if coordinate[1] == self.max_z:
                    temp[self.max_z] += 1
                if coordinate[1] == self.min_z:
                    temp[self.min_z] += 1
            counters.append(temp)
        return counters

    def __set_min_max_values(self, values: (int, int, int, int)):
        self.max_x = values[0]
        self.max_z = values[1]
        self.min_x = values[2]
        self.min_z = values[3]

    def __get_min_max_values(self, result: SolutionGA) -> (int, int, int, int):
        min_x, min_z = 9999999, 9999999
        max_x, max_z = -9999999, -9999999
        for population in result.population:
            population.recalculate()
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
