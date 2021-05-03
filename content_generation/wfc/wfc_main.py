from wfc_state_utility import *
from wfc_states import *
from wfc_variables import State
import random


class WaveFunctionCollapse:

    def run(self, clustered_tiles):
        wfc_states = WfcStates().create_3x3_states()
        # Create state instances
        states: [State] = []
        for key, value in wfc_states[1].items():
            state = State(state_type=key, pattern=[], legal_neighbors=value)
            state.weight = wfc_states[0][key]
            states.append(state)

        # Assign States to tiles
        # TODO: If weights are used then deep copy is needed.
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                tile.assign_states(states)

        # Collapse to random tile
        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                print(tile.entropy)
                tile.states = random.choice(tile.states)

        for cluster in clustered_tiles:
            for tile in cluster.tiles:
                print("- - - - - - - - - - -")
                print(tile)
                print(tile.states)
                print("- - - - - - - - - - -")
            break


    def pattern_from_sample(self):
        pass

    def build_propagator(self):
        pass

    def observe(self):
        pass

    def propagate(self):
        pass
