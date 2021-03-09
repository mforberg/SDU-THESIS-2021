import time

from shared_variables import SolutionGA


class WFCPreprocessing:

    def __init__(self):
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
        # TODO: Handle cases in rectangle where delta X|Z % N != 0
        # TODO: If you check min / max x / z, and you know the edge with most duplicates (e.g. max_x)
        #  you can find direction by adding / subtracting 1 to x by looking at opposite value (e.g. min_X)
        print(f"Counters: max_x | min_x | max_z | min_z")
        print(edge_nodes)
        start = time.time()
        if self.max_x - self.min_x % n != 0:
            # Determine delete x max or min
            for item in edge_nodes:
                if item[self.max_x] > item[self.min_x]:
                    # Remove illegalness
                    print(f"max_x > min_x: {item[self.max_x]} > {item[self.min_x]}")
                    count = 0
                    for solution in result.population:
                        for coord in solution.list_of_coordinates:
                            if coord[1] == self.min_x:
                                solution.list_of_coordinates.remove(coord)
                                count += 1
                    print(f"del count | max_x > min_x: {count}")
                elif item[self.max_x] <= item[self.min_x]:
                    # Remove illegalness
                    print(f"max_x < min_x: {item[self.max_x]} < {item[self.min_x]}")
                    count = 0
                    for solution in result.population:
                        for coord in solution.list_of_coordinates:
                            if coord[0] == self.max_x:
                                solution.list_of_coordinates.remove(coord)
                                count += 1
                    print(f"del count | min_x <= max_x: {count}")
        print(f"Create Tiles Time: {time.time() - start}")
        if self.max_z - self.min_z % n != 0:
            # Determine delete z max or min
            # if edge_nodes[self.max_z] > edge_nodes[self.min_z]:
            #     pass
            # else:
            #     pass

            # Remove illegalness
            for solution in result.population:
                for coord in solution.list_of_coordinates:
                    pass
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
                    temp[self.max_x] += 1
                if coordinate[1] == self.min_z:
                    temp[self.max_x] += 1
            counters.append(temp)
        return counters

    def __set_min_max_values(self, values: (int, int, int, int)):
        self.max_x = values[0]
        self.max_z = values[1]
        self.min_x = values[2]
        self.min_z = values[3]

    def __get_min_max_values(self, max_x: int, max_z: int, min_x: int, min_z: int, result: SolutionGA):
        for population in result.population:
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
