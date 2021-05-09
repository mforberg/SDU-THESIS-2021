from wfc_states import *


def cluster_fully_collapsed(cluster) -> bool:
    for tile in cluster:
        if not tile.collapsed:
            return False
        # if len(tile.states) > 1:
        #     return False
    return True
