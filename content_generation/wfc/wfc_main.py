from math import log

from wfc_utility import *
from wfc_states import *
from models.wfc_models import State, Cluster, Tile
import random
import heapq
import copy


class WaveFunctionCollapse:

    def __init__(self):
        self.heaps = []

    def run(self, clustered_tiles: [Cluster], connection_tiles):
        wfc_states = WfcStates().create_3x3_states()
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

        print("Create state instances")
        # Create state instances
        states: [State] = []
        for key, value in wfc_states[1].items():
            state = State(state_type=key, pattern=[], legal_neighbors=value)
            state.weight = wfc_states[0][key]
            states.append(state)

        # TODO: Remove
        print("- - - - - STATES - - - - -")
        for state in states:
            print(state.type)
            print(state.legal_neighbors)
            print("- - - -")

        print("Assign states to tiles")
        # Assign States to tiles
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                tile.assign_states(copy.deepcopy(states))
                if tile in list_of_connection_tiles:
                    temp_holder = []
                    for state in tile.states:
                        if state.type == "road":
                            temp_holder.append(state)
                    tile.states = temp_holder
                    tile.collapsed = True
                    tile.update_entropy()

        print("Heapify")
        # Heapify list of tiles in each cluster
        self.heaps = clustered_tiles
        for cluster in self.heaps:
            heapq.heapify(cluster.tiles)
            print(f"second call: {len(cluster.tiles)}")

        print("Counter dict")
        counter_dict = {n: 0 for n in range(15)}
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                counter_dict[len(tile.states)] += 1

        print(len(list_of_connection_tiles))
        print(counter_dict)
        # # End of TO DO # # #

        # Propagate connection tile neighbors
        for cluster in self.heaps:
            for tile in cluster.tiles:
                if len(tile.states) == 1:
                    self.propagate(tile)
        # DEBUG
        # for cluster in self.heaps:
        #     for tile in cluster.tiles:
        #         if len(tile.states) == 1:
        #             print("- - - - - - - - - - - - - - - - - - - - ")
        #             print(tile)
        #             print(tile.states)
        #             print(tile.entropy)
        #             print("sssssssssssssssss")
        #             neighbor: Tile
        #             for neighbor in tile.neighbors:
        #                 print(neighbor)
        #                 print(neighbor.entropy)
        #                 print(neighbor.states)
        #                 print("neighbor neighbors")
        #                 for n2 in neighbor.neighbors:
        #                     print(n2)
        #                     print(n2.entropy)
        #                     print(n2.states)
        #                     print("bbbbbbbbbbbbbb")
        #                 print("aaaaaaaaaa")
        #     print("new cluster new cluster new cluster new cluster new cluster ")

        print("Run main algorithm")
        # Run main algorithm on each cluster
        collapsed_tiles = []
        for cluster in self.heaps:
            test = len(cluster.tiles)
            while not cluster_fully_collapsed(cluster=cluster.tiles):

                self.update_entropy_for_all_tiles(cluster=cluster)
                heapq.heapify(cluster.tiles)
                min_entropy_tile = self.observe(cluster.tiles)
                collapsed_tiles.append(min_entropy_tile)
                min_entropy_tile.collapsed = True
                self.propagate(min_entropy_tile)
                print(f"current: {len(cluster.tiles)}, max: {test}")

            # print(collapsed_tiles)
            k = 0
            length = 0
            for tile in cluster.tiles:
                if len(tile.states) > 1:
                    length += 1
                if not tile.collapsed:
                    k += 1
            for item in collapsed_tiles:
                print(item.states)
            print(f"total tiles: {len(cluster.tiles)}")
            print(f"uncollapsed tiles: {k}")
            print(f"tiles states length > 1: {length}")
        print("Return statement")
        return collapsed_tiles

    def observe(self, cluster_tiles):
        # print(f"len pre {len(cluster_tiles)}")
        min_entropy_position: Tile = heapq.heappop(cluster_tiles)
        # print(f"len post {len(cluster_tiles)}")

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
        NORTH, SOUTH, EAST, WEST = (0, 3), (0, -3), (3, 0), (-3, 0)

        while len(stack) > 0:
            current_tile: Tile = stack.pop()

            for neighbor in current_tile.neighbors:
                legal_states_for_neighbor = []
                neighbor_initial_possible_states: [State] = neighbor.states

                # Identify neighbors legal "neighbors neighbor" direction
                existing_directions = self.identify_neighbor_directions(neighbor)

                for neighbor_state in neighbor_initial_possible_states:

                    # Remove states based on states in previous tile
                    state_in_current: [State]
                    for state_in_current in current_tile.states:

                        if neighbor_state.type in state_in_current.legal_neighbors \
                                and neighbor_state not in legal_states_for_neighbor:
                            legal_states_for_neighbor.append(neighbor_state)
                    # print(f"legal_states_for_neighbor: {legal_states_for_neighbor}")
                    # Remove states based on adjacency rules
                    state: State
                    for state in legal_states_for_neighbor:
                        for legal_neighbor, legal_directions in state.legal_neighbors.items():
                            # corner_upper_left = ["N", "S", "E"]
                            temp = []
                            for legal in legal_directions:  # "S", "N", ...
                                if legal == "N":
                                    temp.append(NORTH)
                                elif legal == "S":
                                    temp.append(SOUTH)
                                elif legal == "W":
                                    temp.append(WEST)
                                elif legal == "E":
                                    temp.append(EAST)
                            # print(f"state type: {state.type}")
                            # print(f"existing neighbor directions: {existing_directions}")
                            # print(f"current legal neighbors: {legal_states_for_neighbor}")
                            # print(f"state legal neighbor direction: {state.legal_neighbors.items()}")
                            # print(f"existing_directions[di]:")
                            for di in temp:
                                if not existing_directions[di]:
                                    # print(f"di in existing directions: {di}")
                                    if state in legal_states_for_neighbor:
                                        legal_states_for_neighbor.remove(state)


                if len(legal_states_for_neighbor) > 1:
                    temp = neighbor.states
                    neighbor.states = legal_states_for_neighbor

                    if not set(temp).issubset(set(legal_states_for_neighbor)):
                        if neighbor not in stack:
                            stack.append(neighbor)

    def identify_neighbor_directions(self, neighbor):
        NORTH, SOUTH, EAST, WEST = (0, 3), (0, -3), (3, 0), (-3, 0)
        directions = [NORTH, SOUTH, EAST, WEST]
        existing_directions = {NORTH: False, SOUTH: False, EAST: False, WEST: False}
        neighbor_x = neighbor.nodes[0][0]
        neighbor_z = neighbor.nodes[0][1]
        for neighbors_neighbor in neighbor.neighbors:
            for direction in directions:
                temp_x = neighbor_x + direction[0]
                temp_z = neighbor_z + direction[1]

                if (temp_x, temp_z) in neighbors_neighbor.nodes:
                    existing_directions[direction] = True
        return existing_directions

    def update_entropy_for_all_tiles(self, cluster):
        for tile in cluster.tiles:
            if not tile.collapsed:
                tile.update_entropy()
