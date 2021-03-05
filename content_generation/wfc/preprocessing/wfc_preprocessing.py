from shared_variables import SolutionGA


class WFCPreprocessing:

    def __init__(self):
        self.min_x, self.min_z, self.max_x, self.max_z = 9999999, 9999999, -9999999, -9999999

    def create_tiles(self, result: SolutionGA, n: int):
        # TODO: use n instead of hardcoded values (2, 3)
        # FIND global min+max x, z
        print(result)
        max_x, max_z, min_x, min_z = self.__get_min_max_values(self.max_x, self.max_z, self.min_x, self.min_z, result)

        print(f"width (X):{max_x - min_x}, height (Z): {max_z - min_z}")

        # TODO: Handle cases in rectangle where delta X|Z % N != 0
        print(f"X%N = 2: {(max_x - min_x) % 2}, Z%N = 2: {(max_z - min_z) % 2}")
        print(f"X%N = 3: {(max_x - min_x) % 3}, Z%N = 3: {(max_z - min_z) % 3}")
        counters = []
        for solution_area in result.population:
            temp = {min_x: 0, max_x: 0, min_z: 0, max_z: 0}
            for coordinate in solution_area.list_of_coordinates:
                # (x, y)
                if coordinate[0] == max_x:
                    temp[max_x] += 1
                if coordinate[0] == min_x:
                    temp[min_x] += 1
                if coordinate[1] == max_z:
                    temp[max_x] += 1
                if coordinate[1] == min_z:
                    temp[max_x] += 1
            counters.append(temp)
        # TODO: If you check min / max x / z, and you know the edge with most duplicates (e.g. max_x)
        #  you can find direction by adding / subtracting 1 to x by looking at min_X
        print(f"Counters: max_x | min_x | max_z | min_z")
        print(counters)
        # If there are cases where X|Z % N != find the column or row with least blocks in it then absorb/delete


    def __get_min_max_values(self, max_x, max_z, min_x, min_z, result):
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
