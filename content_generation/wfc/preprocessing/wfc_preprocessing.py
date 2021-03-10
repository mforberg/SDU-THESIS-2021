import time

from shared_variables import SolutionGA


class WFCPreprocessing:

    def __init__(self):
        # this is needed to draw grid over the whole solution so that it can be divided into tiles
        self.min_x, self.min_z = 9999999, 9999999
        self.max_x, self.max_z = -9999999, -9999999

    def create_tiles(self, result: SolutionGA, tile_size: int):

        n = 2  # tile_size

        self.__set_min_max_values(self.__get_min_max_values(result))
        self.__print_modulo_n(n)
        edge_nodes = self.find_edge_node_count(result)
        # TODO: Handle cases in rectangle where delta X|Z % N != 0
        # TODO: If you check min / max x / z, and you know the edge with most duplicates (e.g. max_x)
        #  you can find direction by adding / subtracting 1 to x by looking at opposite value (e.g. min_X)

        # N = 3
        if (self.max_x - self.min_x) % n != 0:
            print(f"x axis is broken {(self.max_x - self.min_x) % n} (N={n})")
            x_deleted_edge = self.max_x
            x_count_min, x_count_max = 0, 0

            for item in edge_nodes:
                x_count_min += item[self.min_x]
                x_count_max += item[self.max_x]

            if x_count_max > x_count_min:
                x_deleted_edge = self.min_x
            count = 0
            for pop in result.population:
                for coord in reversed(pop.list_of_coordinates):
                    if coord[0] == x_deleted_edge:
                        count += 1
                        pop.list_of_coordinates.remove(coord)
            print(f"x deleted: {count}")
        if (self.max_z - self.min_z) % (n) != 0:
            print(f"z axis is broken {(self.max_z - self.min_z) % n} (N={n})")
            z_deleted_edge = self.max_z
            z_count_min, z_count_max = 0, 0

            for item in edge_nodes:
                z_count_min += item[self.min_z]
                z_count_max += item[self.max_z]

            if z_count_max > z_count_min:
                z_deleted_edge = self.min_z
            count = 0
            for pop in result.population:
                for coord in reversed(pop.list_of_coordinates):
                    if coord[1] == z_deleted_edge:
                        count += 1
                        pop.list_of_coordinates.remove(coord)
            print(f"z deleted: {count}")

        self.__set_min_max_values(self.__get_min_max_values(result))
        self.__print_modulo_n(n)

    def __print_modulo_n(self, n):
        print(f"width (X):{self.max_x - self.min_x}, height (Z): {self.max_z - self.min_z}")
        print(f"(N={n}) X%N: {(self.max_x - self.min_x) % n}, Z%N: {(self.max_z - self.min_z) % n}")

    def find_edge_node_count(self, result: SolutionGA) -> [int]:
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

    def __get_min_max_values(self, result: SolutionGA):
        min_x, min_z = 9999999, 9999999
        max_x, max_z = -9999999, -9999999
        for population in result.population:
            population.recalculate()
            min_max_dict = population.min_max_values
            max_x, max_z, min_x, min_z = self.__compare_min_max_values(min_max_dict, max_x, max_z, min_x, min_z)
        return max_x, max_z, min_x, min_z

    # noinspection PyMethodMayBeStatic
    def __compare_min_max_values(self, min_max_dict, max_x, max_z, min_x, min_z):
        if min_max_dict['min_x'] < min_x:
            min_x = min_max_dict['min_x']
        if min_max_dict['max_x'] > max_x:
            max_x = min_max_dict['max_x']
        if min_max_dict['min_z'] < min_z:
            min_z = min_max_dict['min_z']
        if min_max_dict['max_z'] > max_z:
            max_z = min_max_dict['max_z']
        return max_x, max_z, min_x, min_z
