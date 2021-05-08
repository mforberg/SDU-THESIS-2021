from math import log

from wfc_utility import *
from wfc_states import *
from models.wfc_models import State, Cluster, Tile
import random
import heapq
import copy
import sys


class WaveFunctionCollapse:

    def __init__(self):
        self.heaps = []

    def run(self, clustered_tiles: [Cluster], connection_tiles):
        # wfc_states = WfcStates().create_3x3_states()
        # wfc_states = WfcStates().create_simple_3x3_states()
        wfc_states = WfcStates().create_simplest_3x3_states()
        list_of_connection_tiles = []

        # Create list of all tiles assigned to be a connection point (road)
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
        wall_upper = []
        wall_bottom = []
        wall_bottom_and_road = []
        all_states = []

        for state in states:
            if state.type == 'wall_bottom':
                if state not in wall_bottom:
                    wall_bottom.append(copy.deepcopy(state))
                if state not in all_states:
                    all_states.append(copy.deepcopy(state))
            if state.type == 'wall_upper':
                if state not in wall_upper:
                    wall_upper.append(copy.deepcopy(state))
                if state not in wall_bottom_and_road:
                    wall_bottom_and_road.append(copy.deepcopy(state))
                if state not in all_states:
                    all_states.append(copy.deepcopy(state))
            if state.type == 'road':
                if state not in wall_bottom_and_road:
                    wall_bottom_and_road.append(copy.deepcopy(state))
                if state not in all_states:
                    all_states.append(copy.deepcopy(state))

        print("- - - - start of has changed")
        test_tile: Tile = clustered_tiles[0].tiles[0]
        print(f"test_tile.nodes: {test_tile.nodes}")
        print(test_tile.states)
        test_tile_old_states = copy.deepcopy(test_tile.states)
        test_tile.states = wall_bottom
        print(self.has_changed(test_tile_old_states, test_tile.states))
        test_tile.states = wall_upper
        print(self.has_changed(test_tile_old_states, test_tile.states))
        test_tile.states = wall_bottom_and_road
        print(self.has_changed(test_tile_old_states, test_tile.states))
        test_tile.states = all_states
        print(self.has_changed(test_tile_old_states, test_tile.states))
        print(test_tile.states)
        print("- - - - end of has changed")
        print("- - - - - - - - - - - -")
        for neighbor in test_tile.neighbors:
            print(f"neighbor.nodes: {neighbor.nodes}")
            # neighbor.states = copy.deepcopy(wall_bottom_and_road)
            print(f"neighbor.states pre = {neighbor.states}")
            new = self.remove_by_legality(neighbor, test_tile)
            neighbor.states = new
            print(f"neighbor.states post legality = {neighbor.states}")
            new2 = self.remove_by_existing_neighbors(neighbor)
            neighbor.states = new2
            print(f"neighbor.states post existing = {neighbor.states}")
            print("- - - - -")

        input("HOLD THE PHONE")

        print("Heapify")
        # Heapify list of tiles in each cluster
        self.heaps = clustered_tiles
        for cluster in self.heaps:
            heapq.heapify(cluster.tiles)
            # cluster.tiles.sort()

        print("Counter dict")
        counter_dict = {n: 0 for n in range(15)}
        for cluster in self.heaps:
            for tile in cluster.tiles:
                counter_dict[len(tile.states)] += 1

        print(len(list_of_connection_tiles))
        print(counter_dict)
        # # End of TO DO # # #

        # TODO: Probably useless, delete?
        # # Propagate connection tile neighbors
        # for cluster in self.heaps:
        #     for tile in cluster.tiles:
        #         if len(tile.states) == 1:
        #             # TODO: propagate vs propagate2
        #             self.propagate(tile)
        #             # self.propagate2(tile)

        print("Counter dict 2")
        counter_dict = {n: 0 for n in range(15)}
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                counter_dict[len(tile.states)] += 1

        print(len(list_of_connection_tiles))
        print(counter_dict)

        # #  DEBUG
        # for cluster in self.heaps:
        #     for tile in cluster.tiles:
        #         if len(tile.states) == 1:
        #             print("- - - - - - - -  new connection tile - - - - - - - - - - - -")
        #             print(tile)
        #             print(tile.states)
        #             print(tile.entropy)
        #             print("- - - - - - neighbor tile start - - - - - - ")
        #             neighbor: Tile
        #             for neighbor in tile.neighbors:
        #                 print(neighbor)
        #                 print(neighbor.entropy)
        #                 print(neighbor.states)
        #                 print("- - - neighbor neighbors start - - -")
        #                 for n2 in neighbor.neighbors:
        #                     print(n2)
        #                     print(n2.entropy)
        #                     print(n2.states)
        #                     print("- - - - - - - -")
        #                 print("- - - neighbor neighbors end - - -")
        #             print("- - - - - - neighbor tile end - - - - - - ")
        #     print("new cluster new cluster new cluster new cluster new cluster ")
        # inp = input("continue to mail algorithm")
        # print("Run main algorithm")

        # Run main algorithm on each cluster
        collapsed_tiles = []
        for cluster in self.heaps:
            test = len(cluster.tiles)
            collapsed_tiles_in_cluster = []
            #while not cluster_fully_collapsed(cluster=cluster.tiles):
            while len(collapsed_tiles_in_cluster) < test:

                self.update_entropy_for_all_tiles(cluster=cluster)
                heapq.heapify(cluster.tiles)
                # cluster.tiles.sort()
                min_entropy_tile = self.observe(cluster.tiles)
                min_entropy_tile.collapsed = True

                # TODO: propagate vs propagate2
                self.propagate(min_entropy_tile)
                # self.propagate2(min_entropy_tile)

                collapsed_tiles.append(min_entropy_tile)
                collapsed_tiles_in_cluster.append(min_entropy_tile)

                # print(f"current: {len(cluster.tiles)}, max: {test}")
            # print(collapsed_tiles)
            length = 0
            for tile in cluster.tiles:
                if len(tile.states) > 1:
                    length += 1
            # for item in collapsed_tiles:
            #     print(item.states)
            print(f"total tiles in single cluster: {len(cluster.tiles)}")
            print(f"tiles states length > 1: {length}")
            # break
        print("Return statement")
        print(f"total amount of tiles: {sum(counter_dict.values())}")
        print(f"collapsed_tiles={len(collapsed_tiles)}")

        return collapsed_tiles

    def observe(self, cluster_tiles: [Tile]):

        min_entropy_position: Tile = heapq.heappop(cluster_tiles)

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

    def propagate2(self, min_entropy_tile: Tile):
        stack = [min_entropy_tile]
        UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)

        while len(stack) > 0:
            print(f"stack length: {len(stack)}")
            pos: Tile = stack.pop()

            # print("- - - - - - - - - - start of while - - - - - - - - - - - - ")
            # print(f"pos.states={pos.states}")
            # for n in pos.neighbors:
            #     print(f"pos.neighbors.states = {n.states}")
            # print(f"pos.entropy={pos.entropy}")

            possible_patterns = pos.states

            # print("- - - - start of for neighbors - - - -")
            for neighbor in pos.neighbors:
                possible_patterns_at_adjacent = neighbor.states
                # print(f"possible_patterns_at_adjacent = {possible_patterns_at_adjacent}")
                possible_pattern_at_adjacent: State
                for possible_pattern_at_adjacent in possible_patterns_at_adjacent:
                    # print(f"current possible_pattern_at_adjacent (for loop) = {possible_pattern_at_adjacent.type}")

                    is_possible = []  # voodoo shit
                    # go through each pattern at pos if possible_pattern_at_adjacent is legal for any at pos = true

                    pattern: State
                    for pattern in possible_patterns:
                        # print(f"state: {pattern.type} legal_neighbors: {pattern.legal_neighbors}")
                        for legal_neighbor in pattern.legal_neighbors:
                            # print(f"{legal_neighbor} === {possible_pattern_at_adjacent.type} ??? ")
                            if legal_neighbor == possible_pattern_at_adjacent.type:
                                is_possible.append(possible_pattern_at_adjacent)

                    # print(f"is_possible={is_possible}")
                    if is_possible:
                        # delete illegals from neighbor

                        neighbor.states = is_possible
                        if set(possible_patterns_at_adjacent) & (set(is_possible)) == set(possible_patterns_at_adjacent):
                            if neighbor not in stack:
                                # print(f"neighbor ({neighbor.id}) not in stack")
                                stack.append(neighbor)
            # inp = input("Go next")
            # if inp == "cancel":
            #     break

    # def propagate2(self, min_entropy_tile: Tile):
    #     stack = [min_entropy_tile]
    #     UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)
    #
    #     while len(stack) > 0:
    #         print(f"stack length: {len(stack)}")
    #         pos: Tile = stack.pop()
    #
    #         print("- - - - - - - - - - start of while - - - - - - - - - - - - ")
    #         print(f"pos.states={pos.states}")
    #         for n in pos.neighbors:
    #             print(f"pos.neighbors.states = {n.states}")
    #         print(f"pos.entropy={pos.entropy}")
    #
    #         possible_patterns = pos.states
    #
    #         print("- - - - start of for neighbors - - - -")
    #         for neighbor in pos.neighbors:
    #             possible_patterns_at_adjacent = neighbor.states
    #             print(f"possible_patterns_at_adjacent = {possible_patterns_at_adjacent}")
    #             possible_pattern_at_adjacent: State
    #             for possible_pattern_at_adjacent in possible_patterns_at_adjacent:
    #                 print(f"current possible_pattern_at_adjacent (for loop) = {possible_pattern_at_adjacent.type}")
    #                 if len(possible_patterns) > 1:
    #                     print("len(possible_patterns > 1")
    #                     is_possible = False  # voodoo shit
    #                     # go through each pattern at pos if possible_pattern_at_adjacent is legal for any at pos = true
    #
    #                     pattern: State
    #                     for pattern in possible_patterns:
    #                         print(f"state: {pattern.type} legal_neighbors: {pattern.legal_neighbors}")
    #                         for legal_neighbor in pattern.legal_neighbors:
    #                             print(f"{legal_neighbor} === {possible_pattern_at_adjacent.type} ??? ")
    #                             if legal_neighbor == possible_pattern_at_adjacent.type:
    #                                 is_possible = True
    #
    #                 else:
    #                     print("else statement")
    #                     is_possible = False  # voodoo shit
    #                     if possible_pattern_at_adjacent.type in possible_patterns[0].legal_neighbors:
    #                         is_possible = True
    #                 print(f"is_possible={is_possible}")
    #                 if not is_possible:
    #                     # delete illegal shit from neighbor
    #                     still_legal = []
    #
    #                     pattern: State
    #                     for pattern in possible_patterns_at_adjacent:  # neighbors initial states
    #
    #                         legal_neighbor: str
    #                         for possible_pattern in possible_patterns:  # pos possible patterns (previous tile)
    #
    #                             for legal_neighbor in possible_pattern.legal_neighbors:  # legal neighbors to a pattern from pos
    #
    #                                 if legal_neighbor == pattern.type:  # if they same == legal
    #                                     if pattern not in still_legal:  # no dupes
    #                                         still_legal.append(possible_pattern)
    #                     print(f"still_legal: {still_legal}")
    #                     still_legal = list(set(still_legal))
    #                     neighbor.states = still_legal
    #
    #                     if neighbor not in stack:
    #                         print(f"neighbor ({neighbor.id}) not in stack")
    #                         stack.append(neighbor)
    #         # inp = input("Go next")
    #         # if inp == "cancel":
    #         #     break

    def propagate(self, min_entropy_tile: Tile):

        stack = [min_entropy_tile]
        UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)

        while len(stack) > 0:
            current_tile: Tile = stack.pop()

            for neighbor in current_tile.neighbors:
                legal_states_for_neighbor = []
                neighbor_initial_possible_states: [State] = neighbor.states

                # Identify neighbors legal "neighbors neighbor" direction
                existing_directions = self.identify_neighbor_directions(neighbor, current_tile)

                previous_tile_direction = self.find_previous_tile_direction(neighbor, current_tile)
                # TODO: Use bool toggle if all hope is lost


                # TODO: Remove based on neighbor legality alone
                self.remove_by_legality(neighbor, current_tile)

                # TODO: Remove based on existing neighbors
                self.remove_by_existing_neighbors(neighbor)

                # TODO: Remove based on adjacency rules
                self.remove_by_adjacency_rules(neighbor, current_tile)


                    # if not set(temp).issubset(set(legal_states_for_neighbor)):
                    #     neighbor.reassign_states(legal_states_for_neighbor)
                    #     if neighbor not in stack:
                    #         stack.append(neighbor)


    def remove_by_legality(self, neighbor: Tile, current_tile: Tile):

        legal_states_in_neighbor = []

        state_in_current: State
        for state_in_current in current_tile.states:

            # legal_neighbor_state = dict = {state.type: ['dir', 'dir']
            for legal_neighbor_state in state_in_current.legal_neighbors.keys():
                for state in neighbor.states:
                    if state.type == legal_neighbor_state:
                        copy_state = copy.deepcopy(state)
                        if copy_state not in legal_states_in_neighbor:
                            legal_states_in_neighbor.append(copy_state)

        return legal_states_in_neighbor



    def remove_by_existing_neighbors(self, neighbor): # TODO: still test this ohno
        existing_directions = self.find_directions(neighbor, 'should delete this string, fucking retard')
        UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)
        direction_lookup = {'U': UP, 'D': DOWN, 'R': RIGHT, 'L': LEFT}
        inverse_lookup = {'U': 'D', 'D': 'U', 'R': 'L', 'L': 'R'}

        legal_states_for_tile = []

        for state in neighbor.states:
            for legal_dirs_for_state in state.legal_neighbors.values():
                # 'U', 'D', 'L', 'R'
                for legal_dir in legal_dirs_for_state:
                    if existing_directions[direction_lookup[inverse_lookup[legal_dir]]]:
                        if state not in legal_states_for_tile:
                            legal_states_for_tile.append(state)
        return legal_states_for_tile


    def remove_by_adjacency_rules(self, neighbor, current_tile):

        for state_in_current in current_tile.states:
            for legal_dir_for_state in state_in_current.legal_neighbors[state_in_current.type]:



    def has_changed(self, previous_states: [State], new_states: [State]) -> bool:

        result = all(elem in new_states for elem in previous_states)

        return result

    # def propagate(self, min_entropy_tile: Tile):
    #
    #     stack = [min_entropy_tile]
    #     UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)
    #
    #     while len(stack) > 0:
    #         current_tile: Tile = stack.pop()
    #
    #         for neighbor in current_tile.neighbors:
    #             legal_states_for_neighbor = []
    #             neighbor_initial_possible_states: [State] = neighbor.states
    #
    #             # Identify neighbors legal "neighbors neighbor" direction
    #             existing_directions = self.identify_neighbor_directions(neighbor, current_tile)
    #
    #             previous_tile_direction = self.find_previous_tile_direction(neighbor, current_tile)
    #
    #             # TODO: Maybe separate the three steps into own methods
    #             # for / Step 1
    #             # for / Step 2
    #             # for / Step 3
    #
    #             # TODO: Use bool toggle if all hope is lost
    #
    #
    #             for neighbor_state in neighbor_initial_possible_states:
    #                 temp_list = []
    #                 # Remove states based on states in previous tile
    #                 state_in_current: [State]
    #                 for state_in_current in current_tile.states:
    #
    #                     if neighbor_state.type in state_in_current.legal_neighbors \
    #                             and neighbor_state not in temp_list:
    #                         temp_list.append(neighbor_state)
    #
    #                 # print(f"legal_states_for_neighbor: {legal_states_for_neighbor}")
    #                 # Remove states based on adjacency rules
    #                 state: State
    #                 for state in temp_list:
    #                     for state_type, legal_directions in state.legal_neighbors.items():
    #                         # corner_upper_left = ["N", "S", "E"]
    #                         temp = []
    #                         for legal in legal_directions:  # "S", "N", ...
    #                             if legal == "U":
    #                                 temp.append(UP)
    #                             elif legal == "D":
    #                                 temp.append(DOWN)
    #                             elif legal == "L":
    #                                 temp.append(LEFT)
    #                             elif legal == "R":
    #                                 temp.append(RIGHT)
    #                         # print(f"state type: {state.type}")
    #                         # print(f"existing neighbor directions: {existing_directions}")
    #                         # print(f"current legal neighbors: {legal_states_for_neighbor}")
    #                         # print(f"state legal neighbor direction: {state.legal_neighbors.items()}")
    #                         # print(f"existing_directions[di]:")
    #                         # print(f"neighbor.nodes = {neighbor.nodes}")
    #                         # print(f"existing directions: {existing_directions}")
    #                         for di in temp:  # Delete state that has a specific neighbor direction requirement
    #                             # print(f"existing_directions[di]={existing_directions[di]}")
    #                             if not existing_directions[di]:
    #                                 # print(f"di in existing directions: {di}")
    #                                 if state in temp_list:
    #                                     temp_list.remove(state)
    #                         # print(f"previous_tile_direction: {previous_tile_direction}")
    #                         # print(f"legal_directions: {legal_directions}")
    #                         if previous_tile_direction not in legal_directions:  # TODO probably, maybe, idk wrong?
    #                             if state in temp_list:
    #                                 # print(f"state: {state.type}, nodes: {neighbor.nodes} is illegal")
    #                                 # print(f"length of pre temp_list: {len(temp_list)}")
    #                                 temp_list.remove(state)
    #                                 # print(f"length of pre temp_list: {len(temp_list)}")
    #
    #
    #                 legal_states_for_neighbor.extend(temp_list)
    #             # There is a contradiction, and all states removed
    #             if len(legal_states_for_neighbor) == 0:
    #                 pass
    #                 # Solution 1: Run again
    #                 # Solution 2: Backtrack
    #                 # Solution 3: Re-collapse area
    #                 # Solution 4:
    #
    #             if len(legal_states_for_neighbor) > 1:
    #                 temp = neighbor.states
    #
    #
    #                 if not set(temp).issubset(set(legal_states_for_neighbor)):
    #                     neighbor.reassign_states(legal_states_for_neighbor)
    #                     if neighbor not in stack:
    #                         stack.append(neighbor)

    def identify_neighbor_directions(self, neighbor, current_tile):
        UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)
        directions = [UP, DOWN, RIGHT, LEFT]
        existing_directions = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        neighbor_x = neighbor.nodes[0][0]
        neighbor_z = neighbor.nodes[0][1]
        for neighbors_neighbor in neighbor.neighbors:
            for direction in directions:
                temp_x = neighbor_x + direction[0]
                temp_z = neighbor_z + direction[1]

                if (temp_x, temp_z) in neighbors_neighbor.nodes:
                    existing_directions[direction] = True
        return existing_directions

    def find_directions(self, neighbor, identifier: str):
        UP, DOWN, RIGHT, LEFT = (0, -3), (0, 3), (3, 0), (-3, 0)
        directions = [UP, DOWN, RIGHT, LEFT]
        existing_neighbor_directions = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        neighbor_x = neighbor.nodes[0][0]
        neighbor_z = neighbor.nodes[0][1]
        for neighbors_neighbor in neighbor.neighbors:
            print(neighbors_neighbor.nodes)
            for direction in directions:
                new_x = neighbor_x + direction[0]
                new_z = neighbor_z + direction[1]

                if (new_x, new_z) in neighbors_neighbor.nodes:
                    existing_neighbor_directions[(direction[0], direction[1])] = True
        return existing_neighbor_directions

    def update_entropy_for_all_tiles(self, cluster):
        for tile in cluster.tiles:
            if len(tile.states) > 1:
                tile.update_entropy()

    def find_previous_tile_direction(self, neighbor, current_tile):
        existing_directions = {(0, -3): 'D', (0, 3): 'U', (3, 0): 'L', (-3, 0): 'R'}

        delta_difference = (current_tile.nodes[0][0] - neighbor.nodes[0][0],
                            current_tile.nodes[0][1] - neighbor.nodes[0][1])

        return existing_directions[delta_difference]

