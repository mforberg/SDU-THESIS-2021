import copy
from typing import Set, List
from a_star_models import APoint
from variables.a_star_variables import *
import heapq
from tqdm import tqdm


class AStar:

    def __init__(self, surface_dict: dict, fluid_set: set):
        self.surface_dict = surface_dict
        self.fluid_set = fluid_set

    def run(self, blocked_coordinates: Set[APoint], connection_points: List[tuple]) -> List[APoint]:
        total_list_of_road_blocks = []
        dict_of_road_blocks = {}
        for road_network in tqdm(connection_points, desc='A*', leave=True):
            total_list_of_road_blocks.extend(self.connect_point_to_goal(start_points=road_network[0],
                                                                        goal_points=road_network[1],
                                                                        blocked_coordinates=blocked_coordinates,
                                                                        dict_of_road_blocks=dict_of_road_blocks))
        return total_list_of_road_blocks

    def connect_point_to_goal(self, start_points: List[APoint], goal_points: List[APoint],
                              blocked_coordinates: Set[APoint], dict_of_road_blocks: dict) -> List[APoint]:
        open_list = []
        parent_dict = {}
        cost_so_far = dict()
        for point in start_points:
            cost = self.calculate_heuristic(point=point, goals=goal_points)
            cost_so_far[point] = cost
            heapq.heappush(open_list, (cost, point))
        while open_list:
            current_point = heapq.heappop(open_list)[1]
            if current_point in goal_points:
                return self.backtrack(parent_dict=parent_dict, goal_point=current_point,
                                      road_blocks_dict=dict_of_road_blocks)
            if current_point in parent_dict:
                parent = parent_dict[current_point]
            else:
                parent = None
            for neighbor in self.get_neighbors(point=current_point, blocked_coordinates=blocked_coordinates, parent=parent,
                                               road_blocks_dict=dict_of_road_blocks):
                new_cost = cost_so_far[current_point]
                new_cost += self.calculate_path_cost(current_point=current_point, to_point=neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    new_cost += self.calculate_heuristic(point=current_point, goals=goal_points)
                    heapq.heappush(open_list, (new_cost, neighbor))
                    parent_dict[neighbor] = current_point

    def calculate_path_cost(self, current_point: APoint, to_point: APoint) -> int:
        cost = 1
        target_y = to_point.y
        cost += abs(current_point.y - target_y)
        if self.surface_dict[to_point.node].y == target_y:
            if self.surface_dict[to_point.node].block_type in self.fluid_set:
                cost += 3
        else:
            cost += 1 + abs(self.surface_dict[to_point.node].y - target_y)
        return cost

    def calculate_heuristic(self, point: APoint, goals: List[APoint]) -> int:
        smallest = 999999999999999999
        for goal in goals:
            x_diff = abs(point.node[0] - goal.node[0])
            z_diff = abs(point.node[1] - goal.node[1])
            y_diff = abs(point.y - goal.y)
            value = x_diff + z_diff + y_diff
            if value < smallest:
                smallest = value
        return smallest

    def get_neighbors(self, point: APoint, blocked_coordinates: Set[APoint], parent: APoint,
                      road_blocks_dict: dict) -> List[APoint]:
        possible_neighbor_relations = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if parent is not None:
            parent_relation = (parent.node[0] - point.node[0], parent.node[1] - point.node[1])
        else:
            parent_relation = (0, 0)
        neighbors = []
        for possible_neighbor_relation in possible_neighbor_relations:
            if possible_neighbor_relation == parent_relation:
                continue
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
                    if y < surface_y:
                        continue
                    possible_point = APoint(node=possible_neighbor, y=y)
                    #  check blocked coordinates and already placed road blocks
                    if possible_point not in blocked_coordinates:
                        if possible_point.node not in road_blocks_dict:
                            neighbors.append(possible_point)
                        else:
                            y_difference = abs(road_blocks_dict[possible_point.node] - y)
                            if y_difference not in DISALLOWED_Y_DIFFERENCE:
                                neighbors.append(possible_point)
        return neighbors

    def backtrack(self, parent_dict: dict, goal_point: APoint, road_blocks_dict: dict) -> List[APoint]:
        backtracking = []
        current_point = parent_dict[goal_point]
        while current_point in parent_dict:
            backtracking.append(current_point)
            road_blocks_dict[current_point.node] = current_point.y
            current_point = parent_dict[current_point]
        return backtracking
