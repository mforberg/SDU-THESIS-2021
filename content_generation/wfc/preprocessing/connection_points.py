from wfc_tile import *


class ConnectionPoints:

    def __init__(self, clusters: list):
        self.clusters = clusters

    def run(self) -> List[List[tuple]]:
        pass

    # def __find_clusters_touching_each_other_owo(self) -> List[ClustersConnected]:
    #     connected_clusters = []
    #     for cluster in self.clusters:
    #         connected_to = []
    #         for tile in cluster:
    #             list_of_neighbors = self.__find_neighbors_in_other_clusters(tile, cluster)
    #             for neighbor in list_of_neighbors:
    #                 connected_to.append({list_of_neighbors, tile})
    #         connected_clusters.append(ClustersConnected(own_cluster=cluster, connected_to_at_coordinates=None))
    #     return connected_clusters

    def __find_neighbors_in_other_clusters(self, tile, own_cluster) -> List[Tile]:
        list_of_neighbors_in_other_clusters = []
        for neighbor in tile.neighbors:
            for cluster in self.clusters:
                if cluster == own_cluster:
                    continue
                if neighbor in cluster:
                    list_of_neighbors_in_other_clusters.append(neighbor)
        return list_of_neighbors_in_other_clusters
