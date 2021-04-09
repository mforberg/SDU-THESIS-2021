from typing import Set

from variables.map_variables import *
from variables.a_star_variables import *
import heapq


class AStar:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.fluid_set = fluid_set

    def run(self, blocked_coordinates: Set[APoint], connection_points: List[tuple]) -> List[APoint]:
        total_list_of_road_blocks = []
        for road_network in connection_points:
            total_list_of_road_blocks.extend(self.connect_point_to_goal(start_points=road_network[0],
                                                                        goal_points=road_network[1],
                                                                        blocked_coordinates=blocked_coordinates))
        return total_list_of_road_blocks

    def connect_point_to_goal(self, start_points: List[APoint], goal_points: List[APoint],
                              blocked_coordinates: Set[APoint]) -> List[APoint]:
        copy_of_blocked = copy.deepcopy(blocked_coordinates)
        open_list = []
        parent_dict = {}
        cost_so_far = dict()
        for point in start_points:
            cost = self.calculate_heuristic(point=point, goals=goal_points)
            cost_so_far[point] = cost
            heapq.heappush(open_list, (cost, point))
        i = 0
        while open_list:
            i += 1

            current_point = heapq.heappop(open_list)[1]

            if current_point in goal_points:
                print(i)
                print(f"{current_point} in {goal_points}")
                return self.backtrack(parent_dict=parent_dict, goal_point=current_point)

            for neighbor in self.get_neighbors(current_point, copy_of_blocked):
                new_cost = cost_so_far[current_point]
                new_cost += self.calculate_path_cost(current_point=current_point, to_point=neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    new_cost += self.calculate_heuristic(point=current_point, goals=goal_points)
                    heapq.heappush(open_list, (new_cost, neighbor))
                    parent_dict[neighbor] = current_point

    def calculate_path_cost(self, current_point: APoint, to_point: APoint) -> float:
        cost = 1
        target_y = to_point.y
        cost += 2 * abs(current_point.y - target_y)
        if self.surface_dict[to_point.node].y == target_y:
            if self.surface_dict[to_point.node].block_type in self.fluid_set:
                cost += 5
        else:
            cost += 100 * abs(self.surface_dict[to_point.node].y - target_y)
        return cost

    def calculate_heuristic(self, point: APoint, goals: List[APoint]) -> float:
        smallest = 999999999999999999
        for goal in goals:
            x_diff = abs(point.node[0] - goal.node[0])
            z_diff = abs(point.node[1] - goal.node[1])
            y_diff = abs(point.y - goal.y)
            value = x_diff + z_diff + y_diff
            if value < smallest:
                smallest = value
        return smallest

    def get_neighbors(self, point: APoint, blocked_coordinates: Set[APoint]) -> List[APoint]:
        possible_neighbor_relations = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        neighbors = []
        for possible_neighbor_relation in possible_neighbor_relations:
            neighbor_x = point.node[0] + possible_neighbor_relation[0]
            neighbor_z = point.node[1] + possible_neighbor_relation[1]
            possible_neighbor = (neighbor_x, neighbor_z)
            if possible_neighbor in self.surface_dict:
                #  work in y-axis too
                point_y = point.y
                surface_y = self.surface_dict[possible_neighbor].y
                y_relations = [-1, 0, 1]
                for y_relation in y_relations:
                    y = point_y + y_relation
                    if y < surface_y or (y_relation == 0 and possible_neighbor_relation == (0, 0)):
                        continue
                    possible_point = APoint(node=possible_neighbor, y=y)
                    if possible_point not in blocked_coordinates:
                        neighbors.append(possible_point)
        return neighbors

    def backtrack(self, parent_dict: dict, goal_point: APoint) -> List[APoint]:
        backtracking = []
        current_point = parent_dict[goal_point]
        while current_point in parent_dict:
            backtracking.append(current_point)
            current_point = parent_dict[current_point]
        return backtracking
