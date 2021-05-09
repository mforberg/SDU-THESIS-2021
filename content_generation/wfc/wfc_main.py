from math import log
from typing import List

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

    def run(self, clustered_tiles: List[Cluster], connection_tiles: tuple):
        wfc_states = WfcStates().create_simplest_3x3_states()
        list_of_connection_tiles = []

        for item in connection_tiles:
            list_of_connection_tiles.append(item[0])
            list_of_connection_tiles.append(item[1])
        # list_of_connection_tiles = [item for t in connection_tiles for item in t]

        # Remove illegal neighbors AGAIN???
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                for neighbor in tile.neighbors:
                    if tile.cluster_assignment != neighbor.cluster_assignment:
                        tile.remove_neighbor(neighbor)

        # Create state instances
        states: List[State] = []
        for key, value in wfc_states[1].items():
            current_needs = wfc_states[2][key]
            # print(current_needs)
            state = State(state_type=key, pattern=[], legal_neighbors=value, needs=current_needs)
            state.weight = wfc_states[0][key]
            states.append(state)

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

        # Heapify list of tiles in each cluster
        self.heaps = clustered_tiles
        for cluster in self.heaps:
            heapq.heapify(cluster.tiles)

        counter_dict = {n: 0 for n in range(len(states)+1)}
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                counter_dict[len(tile.states)] += 1

        # # End of TO DO # # #

        # # Propagate connection tile neighbors
        # for cluster in self.heaps:
        #     for tile in cluster.tiles:
        #         if len(tile.states) == 1:
        #             self.propagate(tile)

        amount_of_tiles = 0
        for cluster in self.heaps:
            for _ in cluster.tiles:
                amount_of_tiles += 1

        # Run main algorithm on each cluster
        collapsed_tiles = []
        for cluster in self.heaps:
            while not cluster_fully_collapsed(cluster=cluster.tiles):
                self.update_entropy_for_all_tiles(cluster=cluster)
                heapq.heapify(cluster.tiles)
                min_entropy_tile = self.__observe(cluster.tiles)
                collapsed_tiles.append(min_entropy_tile)
                min_entropy_tile.collapsed = True
                self.propagate(min_entropy_tile)

        print(f"Successfully collapsed tiles: {len(collapsed_tiles)}/{amount_of_tiles}")
        self.print_state_type_count(collapsed_tiles)
        return collapsed_tiles

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
