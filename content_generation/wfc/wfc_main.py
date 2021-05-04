from wfc_utility import *
from wfc_states import *
from models.wfc_models import State, Cluster, Tile
import random
import heapq


class WaveFunctionCollapse:

    def run(self, clustered_tiles, connection_tiles):
        wfc_states = WfcStates().create_3x3_states()
        list_of_connection_tiles = []
        for item in connection_tiles:
            list_of_connection_tiles.append(item[0])
            list_of_connection_tiles.append(item[1])
        #list_of_connection_tiles = [item for t in connection_tiles for item in t]
        print("Create state instances")
        k = 0
        c: Cluster
        for c in clustered_tiles:
            k += len(c.tiles)
        print(f"Tile Count: {k}")


        # Create state instances
        states: [State] = []
        for key, value in wfc_states[1].items():
            state = State(state_type=key, pattern=[], legal_neighbors=value)
            state.weight = wfc_states[0][key]
            states.append(state)
        print("Assign states to tiles")


        # Assign States to tiles
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                tile.assign_states(states)
                # TODO: comment back in later, is problem Jonas
                # if tile in list_of_connection_tiles:
                #     temp_holder = []
                #     for state in tile.states:
                #         if state.type == "road":
                #             temp_holder.append(state)
                #     tile.states = temp_holder
                #     tile.update_entropy()
        print("Counter dict")


        # TODO: Show jonas
        counter_dict = {n: 0 for n in range(15)}
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                counter_dict[len(tile.states)] += 1
        print(list_of_connection_tiles)
        print(len(list_of_connection_tiles))
        print(counter_dict)
        # # # End of TO DO # # #

        # # Propagate connection tile neighbors
        # for cluster in clustered_tiles:
        #     for tile in cluster.tiles:
        #         if len(tile.states) == 1:
        #             neighbor_tile: Tile
        #             for neighbor_tile in tile.neighbors:
        #                 temp = []
        #                 for n in tile.neighbors:
        #                     temp.append(n)
        #                 print("- - - - - - - -")
        #                 print(neighbor_tile.states)
        #                 print(neighbor_tile.entropy)
        #                 neighbor_tile.states = temp
        #                 neighbor_tile.update_entropy()
        #                 print(neighbor_tile.states)
        #                 print(neighbor_tile.entropy)
        #                 print("- - - - - - - -")

        print("Heapify")
        # Heapify list of tiles in each cluster
        for cluster in clustered_tiles:
            heapq.heapify(cluster.tiles)

        print("Run main algorithm")
        # Run main algorithm on each cluster
        collapsed_tiles = []
        for cluster in clustered_tiles:
            while not cluster_fully_collapsed(cluster=cluster.tiles):
                min_entropy_tile = self.observe(cluster.tiles)
                collapsed_tiles.append(min_entropy_tile)
                self.propagate(min_entropy_tile)
        print("Return statement")
        return collapsed_tiles


    def observe(self, cluster):
        """
        2. Choose pattern based on frequency
        3. Collapse to that
        @param cluster:
        @return:
        """

        min_entropy_position: Tile = heapq.heappop(cluster)

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

        # TODO: Infinite loop me thinks
        stack = [min_entropy_tile]

        while len(stack) > 0:
            current_tile: Tile = stack.pop()
            possible_states = current_tile.states

            for neighbor in current_tile.neighbors:
                legal_states_for_neighbor = []
                neighbor_possible_states: [State] = neighbor.states

                for state in neighbor_possible_states:
                    for legal_neighbor in current_tile.neighbors:
                        for s2 in legal_neighbor.states:
                            if state == s2:
                                if state not in legal_states_for_neighbor:
                                    legal_states_for_neighbor.append(state)
                temp = neighbor.states
                neighbor.states = legal_states_for_neighbor

                if not set(legal_states_for_neighbor).issubset(set(temp)):
                    if neighbor not in stack:
                        stack.append(neighbor)
                # for state in neighbor.states:
                #     if state in possible_states:
                #         temp.append(state)
                # neighbor.states = temp
                #
                # if neighbor not in stack:
                #     stack.append(neighbor)
