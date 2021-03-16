from variables.map_variables import *
import heapq


class AStar:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.fluid_set = fluid_set

    def run(self, blocked_coordinates: set, connection_points: List[tuple]):
        pass

    def connect_point_to_goal(self, start_point: tuple, goal_point: tuple, blocked_coordinates: set) -> List[tuple]:
        open_list = []
        parent_dict = {}
        close_set = set
        heapq.heappush(open_list, (0, start_point))
        while open_list:
            current_point = heapq.heappop(open_list)[1]

            if current_point == goal_point:
                return self.backtrack(parent_dict=parent_dict, start_point=start_point, goal_point=goal_point)

            for neighbor in self.get_neighbors(current_point):
                neighbor_block = self.surface_dict[neighbor]
                

    def calculate_heuristic(self, point1: tuple, point2: tuple) -> float:
        x_diff = abs(point1[0] - point2[0])
        z_diff = abs(point1[1] - point2[1])
        y_diff = abs(self.surface_dict[point1]['y'] - self.surface_dict[point2]['y'])
        return x_diff + z_diff + y_diff

    def get_neighbors(self, point: tuple) -> List[tuple]:
        possible_neighbor_relations = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        for possible_neighbor_relation in possible_neighbor_relations:
            neighbor_x = point[0] + possible_neighbor_relation[0]
            neighbor_z = point[1] + possible_neighbor_relation[1]
            possible_neighbor = (neighbor_x, neighbor_z)
            if possible_neighbor in self.surface_dict:
                neighbors.append(possible_neighbor)
        return neighbors

    def backtrack(self, parent_dict: dict, start_point: tuple, goal_point: tuple) -> List[tuple]:
        backtracking = []
        current_node = goal_point
        while current_node in parent_dict:
            backtracking.append(current_node)
            current_node = parent_dict[current_node]
        backtracking.append(start_point)
        return backtracking
