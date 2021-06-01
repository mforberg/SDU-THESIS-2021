from wfc_states import *


def cluster_fully_collapsed(cluster) -> bool:
    for tile in cluster:
        if not tile.collapsed:
            return False
    return True
