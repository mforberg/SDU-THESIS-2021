from variables.shared_variables import *
# pip install -U scikit-learn
from sklearn.cluster import KMeans
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
import numpy as np
from numpy import linalg
import math
import statistics


class KMeansClustering:
    minimum_length_of_centroid = 0

    def run(self, first_ga_result: SolutionGA):
        converted_coordinates = self.combine_the_lists_and_convert_to_list_of_list(first_ga_result)
        centroids, centroid_centers = self.find_centroids(list_of_points=converted_coordinates)
        self.calculate_minimum_length_of_centroid(centroids=centroids)
        self.combine_small_centroid_to_others(centroids=centroids, centroid_centers=centroid_centers)
        return centroids

    def combine_small_centroid_to_others(self, centroids: List[List[list]], centroid_centers: List[list]):
        skip_indexes = set()
        remove_index = []
        for x in range(0, len(centroids)):
            current_centroid = centroids[x]
            if len(current_centroid) < self.minimum_length_of_centroid:
                index = self.find_nearest_centroid_center(centroid_centers=centroid_centers, current_index=x,
                                                          skip_set=skip_indexes)
                remove_index.append(x)
                skip_indexes.add(x)
                centroids[index].extend(current_centroid)
        for index in remove_index[::-1]:
            centroids.pop(index)

    def calculate_minimum_length_of_centroid(self, centroids: List[List[list]]):
        length_list = []
        max_length = 0
        for index in centroids:
            length_list.append(len(index))
            if len(index) > max_length:
                max_length = len(index)
        median = statistics.median(length_list)
        self.minimum_length_of_centroid = median + math.floor((max_length - median)/2)

    def find_nearest_centroid_center(self, centroid_centers: List[list], current_index: int, skip_set: set) -> int:
        closest = None
        shortest_distance = 100000
        center = [centroid_centers[current_index][0], centroid_centers[current_index][1]]
        for i in range(0, len(centroid_centers)):
            if i == current_index or i in skip_set:
                continue
            current_center_x = centroid_centers[i][0]
            current_center_z = centroid_centers[i][1]
            distance = math.sqrt(math.pow(center[0] - current_center_x, 2) + math.pow(center[1] - current_center_z, 2))
            if distance < shortest_distance:
                shortest_distance = distance
                closest = i
        return closest

    def combine_the_lists_and_convert_to_list_of_list(self, ga_solution: SolutionGA) -> List[list]:
        total_list_of_coordinates = []
        for area in ga_solution.population:
            for index in area.list_of_coordinates:
                total_list_of_coordinates.append([index[0], index[1]])
        return total_list_of_coordinates

    def find_centroids(self, list_of_points: List[list]) -> (List[List[list]], List[list]):
        k = self.elbow_method(list_of_points=list_of_points)
        k_means = KMeans(n_clusters=k).fit(list_of_points)
        cluster_association = k_means.labels_  # array([1, 1, 1, 0, 0, 0]

        list_of_clusters = [[] for _ in range(k)]

        for i in range(len(list_of_points)):
            list_of_clusters[cluster_association[i]].append(list_of_points[i])

        cluster_centers = k_means.cluster_centers_
        return list_of_clusters, cluster_centers

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
