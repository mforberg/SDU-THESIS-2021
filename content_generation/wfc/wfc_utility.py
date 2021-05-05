from wfc_states import *


def cluster_fully_collapsed(cluster):
    for tile in cluster:
        if len(tile.states) > 1:
            return False
    return True
