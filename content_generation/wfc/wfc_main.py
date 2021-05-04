from wfc_utility import *
from wfc_states import *
from wfc_variables import State
import random
import heapq


class WaveFunctionCollapse:

    def run(self, clustered_tiles, connection_tiles):
        wfc_states = WfcStates().create_3x3_states()
        list_of_connection_tiles = [item for t in connection_tiles for item in t]

        # Create state instances
        states: [State] = []
        for key, value in wfc_states[1].items():
            state = State(state_type=key, pattern=[], legal_neighbors=value)
            state.weight = wfc_states[0][key]
            states.append(state)

        # Assign States to tiles
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                tile.assign_states(states)
                if tile in list_of_connection_tiles:
                    temp_holder = []
                    for state in tile.states:
                        if state.type == "road":
                            temp_holder.append(state)
                    tile.states = temp_holder
                    tile.update_entropy()

        # Heapify list of tiles in each cluster
        for cluster in clustered_tiles:
            heapq.heapify(cluster.tiles)

        # Run main algorithm on each cluster
        for cluster in clustered_tiles:
            while not cluster_fully_collapsed(cluster=cluster.tiles):
                min_entropy_tile = self.observe(cluster.tiles)
                self.propagate(min_entropy_tile)


    def observe(self, cluster):
        """
        2. Choose pattern based on frequency
        3. Collapse to that
        @param lowest_entropy:
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
                min_entropy_position.states = state
                break
            else:
                target -= state.weight

        return min_entropy_position

    def propagate(self, min_entropy_tile):
        pass
