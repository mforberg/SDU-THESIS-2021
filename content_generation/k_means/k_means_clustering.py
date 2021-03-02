from variables.shared_variables import *
# pip install -U scikit-learn
from sklearn.cluster import KMeans
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
" For testing "
import numpy as np
from numpy import linalg


class KMeansClustering:
    def run(self, first_ga_result: SolutionGA):
        converted_coordinates = self.combine_the_lists_and_convert_to_list_of_list(first_ga_result)
        centroids = self.find_centroids(number_of_clusters=2, list_of_points=converted_coordinates)
        return centroids

    def combine_the_lists_and_convert_to_list_of_list(self, ga_solution: SolutionGA) -> List[list]:
        total_list_of_coordinates = []
        for area in ga_solution.population:
            for index in area.list_of_coordinates:
                total_list_of_coordinates.append([index[0], index[1]])
        return total_list_of_coordinates

    def find_centroids(self, number_of_clusters: int, list_of_points: List[list]) -> List[List[list]]:
        # k = self.elbow_method(list_of_points=list_of_points)
        k = 6
        print(k)
        k_means = KMeans(n_clusters=k).fit(list_of_points)
        cluster_association = k_means.labels_  # array([1, 1, 1, 0, 0, 0]

        list_of_clusters = [[] for x in range(k)]

        for i in range(len(list_of_points)):
            list_of_clusters[cluster_association[i]].append(list_of_points[i])
        return list_of_clusters

    def elbow_method(self, list_of_points: List[list]) -> int:
        wcss = []  # Within-Cluster-Sum-of-Squares
        max_cluster = 11
        if len(list_of_points) < max_cluster:
            max_cluster = len(list_of_points)
        for i in range(1, max_cluster+1):  # 1 inclusive to 11
            kmeans = KMeans(n_clusters=i)
            kmeans = kmeans.fit(list_of_points)
            wcss.append(kmeans.inertia_)
        p1 = ([1, wcss[0]])
        p1 = np.asarray(p1)
        p2 = np.asarray([max_cluster, wcss[max_cluster-1]])
        p2 = np.asarray(p2)

        current_max_distance = 0
        current_n = 0
        for i in range(0, max_cluster-1):
            p3 = ([i + 1, wcss[i]])
            p3 = np.asarray(p3)
            d = linalg.norm(np.cross(p2 - p1, p1 - p3)) / linalg.norm(p2 - p1)
            if current_max_distance < d:
                current_n = i
        return current_n
