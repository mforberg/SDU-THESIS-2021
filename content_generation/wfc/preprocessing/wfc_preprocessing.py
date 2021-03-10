import time

from shared_variables import SolutionGA


class WFCPreprocessing:

    def __init__(self):
        # this is needed to draw grid over the whole solution so that it can be divided into tiles
        self.min_x, self.min_z = 9999999, 9999999
        self.max_x, self.max_z = -9999999, -9999999

    def create_tiles(self, result: SolutionGA, tile_size: int):

        # TODO: use n instead of hardcoded values (2, 3)
        n = 2  # tile_size

        # FIND global min+max x, z
        print(result)
        self.__set_min_max_values(self.__get_min_max_values(self.max_x, self.max_z, self.min_x, self.min_z, result))
        self.__print_modulo_n()
        edge_nodes = self.find_edge_node_count(result)
        print(self.min_x, self.max_x, self.min_z, self.max_z)
        # TODO: Handle cases in rectangle where delta X|Z % N != 0
        # TODO: If you check min / max x / z, and you know the edge with most duplicates (e.g. max_x)
        #  you can find direction by adding / subtracting 1 to x by looking at opposite value (e.g. min_X)
        print(f"Counters: max_x | min_x | max_z | min_z")
        print(edge_nodes)

        # N = 2
        # TODO: should just use n, but need to test both even and uneven cases
        if (self.max_x - self.min_x) % n != 0:
            print(f"x axis is broken {(self.max_x - self.min_x) % n} (N={n})")

        if (self.max_z - self.min_z) % n != 0:
            print(f"z axis is broken {(self.max_z - self.min_z) % n} (N={n})")

        # N = 3
        if (self.max_x - self.min_x) % (n+1) != 0:
            print(f"x axis is broken {(self.max_x - self.min_x) % n} (N={n+1})")
            x_deleted_edge = self.max_x
            x_count_min, x_count_max = 0, 0

            for item in edge_nodes:
                x_count_min += item[self.min_x]
                x_count_max += item[self.max_x]

            if x_count_max > x_count_min:
                x_deleted_edge = self.min_x
            print(f"x count_min: {x_count_min}, x count_max: {x_count_max}")
            count = 0
            for pop in result.population:
                for coord in reversed(pop.list_of_coordinates):
                    if coord[0] == x_deleted_edge:
                        count += 1
                        pop.list_of_coordinates.remove(coord)
            print(f"x deleted: {count}")
        if (self.max_z - self.min_z) % (n+1) != 0:
            print(f"z axis is broken {(self.max_z - self.min_z) % n} (N={n+1})")
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
            print(f"z count_min: {z_count_min}, z count_max: {z_count_max}")

        self.__set_min_max_values(self.__get_min_max_values(self.max_x, self.max_z, self.min_x, self.min_z, result))
        self.__print_modulo_n()
        edge_nodes2 = self.find_edge_node_count(result)
        print(f"Counters: max_x | min_x | max_z | min_z")
        print(edge_nodes2)
        print(self.min_x, self.max_x, self.min_z, self.max_z)
        # If there are cases where X|Z % N != find the column or row with least blocks in it then absorb/delete

    def __print_modulo_n(self):
        print(f"width (X):{self.max_x - self.min_x}, height (Z): {self.max_z - self.min_z}")
        print(f"X%N = 2: {(self.max_x - self.min_x) % 2}, Z%N = 2: {(self.max_z - self.min_z) % 2}")
        print(f"X%N = 3: {(self.max_x - self.min_x) % 3}, Z%N = 3: {(self.max_z - self.min_z) % 3}")

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

    def __get_min_max_values(self, max_x: int, max_z: int, min_x: int, min_z: int, result: SolutionGA):
        # TODO: find out why the fuck stupid shit no update min max x z
        for population in result.population:
            population.recalculate_min_max_mass()
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
