from math import log
from typing import List

from wfc_contradiction_error import ContradictionException
from wfc_utility import *
from wfc_states import *
from models.wfc_models import State, Cluster, Tile
import random
import heapq
import copy
import pprint


class WaveFunctionCollapse:

    def __init__(self, tile_size: int):
        self.heaps = []
        self.NORTH, self.SOUTH, self.EAST, self.WEST = (0, -tile_size), (0, tile_size), (tile_size, 0), (-tile_size, 0)
        self.failed_runs = 0
        self.collapsed_tiles_test = []
        self.connection_tiles = []
        self.states = []

    def run(self, clustered_tiles: List[Cluster], connection_tiles: tuple):
        wfc_state_config = WfcStates().create_simplest_3x3_states()

        # list_of_connection_tiles = [item for t in connection_tiles for item in t]
        list_of_connection_tiles = self.__create_list_of_connection_tiles(connection_tiles)
        self.connection_tiles.extend(list_of_connection_tiles)

        self.__remove_illegal_neighbors(clustered_tiles)

        # Create state instances
        states = self.__create_states(wfc_state_config)
        self.states.extend(states)

        self.__assign_states_to_tiles(clustered_tiles, list_of_connection_tiles, states)

        # Heapify list of tiles in each cluster
        self.heaps = clustered_tiles

        # Create heap for each cluster, sorted by entropy
        for cluster in self.heaps:
            heapq.heapify(cluster.tiles)

        amount_of_tiles = 0
        for cluster in self.heaps:
            amount_of_tiles += len(cluster.tiles)

        # Run main algorithm on each cluster
        self.__wfc_run_loop()

        print(f"Successfully collapsed tiles: {len(self.collapsed_tiles_test)}/{amount_of_tiles}")
        self.print_state_type_count(self.collapsed_tiles_test)
        return self.collapsed_tiles_test

    def __wfc_run_loop(self):

        tile_holder = {cluster.id: [] for cluster in self.heaps}

        for cluster in self.heaps:
            try:
                collapsed_tiles = []
                while not cluster_fully_collapsed(cluster=cluster.tiles):

                    if self.__contains_contractiction(cluster):
                        raise ContradictionException

                    self.update_entropy_for_all_tiles(cluster=cluster)
                    heapq.heapify(cluster.tiles)
                    min_entropy_tile = self.__observe(cluster.tiles)
                    tile_holder[cluster.id].append(min_entropy_tile)
                    collapsed_tiles.append(min_entropy_tile)
                    min_entropy_tile.collapsed = True
                    self.propagate(min_entropy_tile)

                self.collapsed_tiles_test.extend(collapsed_tiles)

            except ContradictionException:
                cluster.tiles.extend(tile_holder[cluster.id])
                tile_holder[cluster.id] = []
                print(f"Cluster '{cluster.tiles[0].district_type}' Failed")
                self.__reset_tiles(cluster, self.connection_tiles, self.states)
                self.__wfc_run_loop()

    def __reset_tiles(self, cluster, list_of_connection_tiles, states):

        for tile in cluster.tiles:
            tile.assign_states(copy.deepcopy(states))
            tile.collapsed = False
            if tile in list_of_connection_tiles:
                temp_holder = []
                for state in tile.states:
                    if state.state_type == "road":
                        temp_holder.append(state)
                tile.states = temp_holder
                tile.collapsed = True
                tile.update_entropy()

    def __contains_contractiction(self, cluster):
        for tile in cluster.tiles:
            if len(tile.states) == 0:
                return True
        return False

    def __assign_states_to_tiles(self, clustered_tiles, list_of_connection_tiles, states):
        # Assign States to tiles
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                tile.assign_states(copy.deepcopy(states))
                if tile in list_of_connection_tiles:
                    temp_holder = []
                    for state in tile.states:
                        if state.state_type == "road":
                            temp_holder.append(state)
                    tile.states = temp_holder
                    tile.collapsed = True
                    tile.update_entropy()

    def __create_states(self, wfc_state_config):
        states: List[State] = []
        for key, value in wfc_state_config[1].items():
            current_needs = wfc_state_config[2][key]
            # print(current_needs)
            state = State(state_type=key, pattern=[], legal_neighbors=value, needs=current_needs)
            state.weight = wfc_state_config[0][key]
            states.append(state)
        return states

    def __create_list_of_connection_tiles(self, connection_tiles):
        list_of_connection_tiles = []
        for item in connection_tiles:
            list_of_connection_tiles.append(item[0])
            list_of_connection_tiles.append(item[1])
        return list_of_connection_tiles

    def __remove_illegal_neighbors(self, clustered_tiles):
        # Remove illegal neighbors AGAIN???
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                for neighbor in tile.neighbors:
                    if tile.cluster_assignment != neighbor.cluster_assignment:
                        tile.remove_neighbor(neighbor)

    def print_state_type_count(self, collapsed_tiles):

        counter_dict = {}
        for tile in collapsed_tiles:
            for state in tile.states:
                if state.state_type in counter_dict.keys():
                    counter_dict[state.state_type] += 1
                else:
                    counter_dict[state.state_type] = 1
        pprint.pprint(counter_dict)

    def __observe(self, cluster_tiles: List[Tile]) -> Tile:
        min_entropy_position = heapq.heappop(cluster_tiles)

        # Calculate upper bound for state probability
        max_probability = 0
        for state in min_entropy_position.states:
            max_probability += state.weight

        # Make weighted choice
        random_float = random.random()
        target = random_float * max_probability
        for state in min_entropy_position.states:
            if state.weight >= target:
                min_entropy_position.states = [state]
                break
            else:
                target -= state.weight

        return min_entropy_position

    def propagate(self, min_entropy_tile: Tile):

        stack = [min_entropy_tile]

        while len(stack) > 0:
            current_tile = stack.pop()
            for neighbor in current_tile.neighbors:
                if len(neighbor.states) == 1:
                    continue
                length_of_old = len(neighbor.states)
                legal_states_for_neighbor = self.__get_neighbors_allowed_states(current_tile=current_tile,
                                                                                neighbor_tile=neighbor)
                neighbor.states = legal_states_for_neighbor
                length_of_new = len(legal_states_for_neighbor)
                if length_of_old > length_of_new:
                    # TODO: neighbor not in stack?
                    stack.append(neighbor)

    def __get_neighbors_allowed_states(self, current_tile: Tile, neighbor_tile: Tile) -> List[State]:
        illegal_states_for_neighbor = set()
        neighbor_initial_possible_states = copy.deepcopy(neighbor_tile.states)

        # TODO: FIX current!
        current = [current_tile]
        for neighbor_state in neighbor_initial_possible_states:
            if not self.__is_state_allowed_based_on_neighbor(state=neighbor_state, neighbors=current,
                                                             current_tile=neighbor_tile):
                illegal_states_for_neighbor.add(neighbor_state)
                continue
            if not self.__is_state_allowed_based_on_missing_neighbors(state=neighbor_state,
                                                                      neighbors=neighbor_tile.neighbors,
                                                                      current=neighbor_tile):
                illegal_states_for_neighbor.add(neighbor_state)
                continue
        legal_states = []
        for state in neighbor_initial_possible_states:
            if state not in illegal_states_for_neighbor:
                legal_states.append(state)
        return legal_states

    def __is_state_allowed_based_on_missing_neighbors(self, current: Tile, state: State, neighbors: List[Tile]) -> bool:
        for need in state.needs:
            need_met = False
            for neighbor in neighbors:
                orientation = self.__find_previous_tile_direction(neighbor=current, current_tile=neighbor)
                if need == orientation:
                    need_met = True
            if not need_met:
                return False
        return True

    def __is_state_allowed_based_on_neighbor(self, current_tile: Tile, state: State, neighbors: List[Tile]) -> bool:
        for neighbor in neighbors:
            neighbor_allow = False
            orientation = self.__find_previous_tile_direction(neighbor=neighbor, current_tile=current_tile)
            for neighbor_state in neighbor.states:
                for legal_neighbor, legal_directions in neighbor_state.legal_neighbors.items():
                    if state.state_type == legal_neighbor:
                        if orientation in legal_directions:
                            neighbor_allow = True
            if not neighbor_allow:
                return False
        return True

    def __find_previous_tile_direction(self, neighbor, current_tile) -> str:
        existing_directions = {self.NORTH: 'N', self.SOUTH: 'S', self.WEST: 'W', self.EAST: 'E'}

        delta_difference = (current_tile.nodes[0][0] - neighbor.nodes[0][0],
                            current_tile.nodes[0][1] - neighbor.nodes[0][1])

        return existing_directions[delta_difference]

    def update_entropy_for_all_tiles(self, cluster):
        for tile in cluster.tiles:
            if not tile.collapsed:
                tile.update_entropy()
