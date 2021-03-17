from variables.map_variables import *
import heapq


class AStar:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.fluid_set = fluid_set

    def run(self, blocked_coordinates: set, connection_points: List[List[tuple]]) -> List[tuple]:
        total_list_of_road_blocks = []
        for road_network in connection_points:
            total_list_of_road_blocks.extend(self.connect_point_to_goal(start_point=road_network[0],
                                                                        goal_point=road_network[1],
                                                                        blocked_coordinates=blocked_coordinates))
        return total_list_of_road_blocks

    def connect_point_to_goal(self, start_point: tuple, goal_point: tuple, blocked_coordinates: set) -> List[tuple]:
        open_list = []
        parent_dict = {}
        cost_so_far = {start_point: 0}
        heapq.heappush(open_list, (0, start_point))
        while open_list:
            current_point = heapq.heappop(open_list)[1]

            if current_point == goal_point:
                return self.backtrack(parent_dict=parent_dict, start_point=start_point, goal_point=goal_point)

            for neighbor in self.get_neighbors(current_point, blocked_coordinates):
                new_cost = cost_so_far[current_point]
                new_cost += self.calculate_path_cost(current_point=current_point, to_point=neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    new_cost += self.calculate_heuristic(point1=current_point, point2=neighbor)
                    heapq.heappush(open_list, (new_cost, neighbor))
                    parent_dict[neighbor] = current_point

    def calculate_path_cost(self, current_point: tuple, to_point: tuple) -> float:
        cost = 1
        cost += 5 * abs(self.surface_dict[current_point]['y'] - self.surface_dict[to_point]['y'])
        if self.surface_dict[to_point]['type'] in self.fluid_set:
            cost += 5
        return cost

    def calculate_heuristic(self, point1: tuple, point2: tuple) -> float:
        x_diff = abs(point1[0] - point2[0])
        z_diff = abs(point1[1] - point2[1])
        y_diff = abs(self.surface_dict[point1]['y'] - self.surface_dict[point2]['y'])
        return x_diff + z_diff + y_diff

    def get_neighbors(self, point: tuple, blocked_coordinates: set) -> List[tuple]:
        possible_neighbor_relations = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        for possible_neighbor_relation in possible_neighbor_relations:
            neighbor_x = point[0] + possible_neighbor_relation[0]
            neighbor_z = point[1] + possible_neighbor_relation[1]
            possible_neighbor = (neighbor_x, neighbor_z)
            if possible_neighbor in self.surface_dict:
                if possible_neighbor not in blocked_coordinates:
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
