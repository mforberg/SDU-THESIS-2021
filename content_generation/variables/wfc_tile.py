from typing import List
from uuid import uuid4


class Tile:

    def __init__(self, nodes: List[tuple]):
        self.id: str = str(uuid4())
        self.nodes: List[tuple] = nodes
        # self.neighbor: List[Tile] = neighbors

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.id[:8]}, Nodes:\n {self.nodes}>"


class ConnectedToClusterAtCoordinates:

    def __init__(self, cluster: List[Tile], tiles: List[Tile]):
        pass


# class ClustersConnected:
#
#     def __init__(self, own_cluster: List[Tile], connected_to_at_coordinates: List[{List[Tile], List[Tile]}]):
#         self.own_cluster = own_cluster
#         self.connected_clusters = connected_to_at_coordinates

