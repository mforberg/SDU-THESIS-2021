from variables.shared_variables import *
# pip install -U scikit-learn
from sklearn.cluster import KMeans
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html


class KMeansClustering:
    def run(self, first_ga_result: SolutionGA):
        converted_coordinates = self.combine_the_lists_and_convert_to_list_of_list(first_ga_result)
        centroids = self.find_centroids(number_of_clusters=2, list_of_points=converted_coordinates)
        print(len(centroids))

    def combine_the_lists_and_convert_to_list_of_list(self, ga_solution: SolutionGA) -> List[list]:
        total_list_of_coordinates = []
        for area in ga_solution.population:
            for index in area.list_of_coordinates:
                total_list_of_coordinates.append([index[0], index[1]])
        return total_list_of_coordinates

    def find_centroids(self, number_of_clusters: int, list_of_points: List[list]) -> List[List[list]]:
        k = number_of_clusters
        k_means = KMeans(n_clusters=k).fit(list_of_points)
        cluster_association = k_means.labels_  # array([1, 1, 1, 0, 0, 0]

        list_of_clusters = [[] for x in range(k)]

        for i in range(len(list_of_points)):
            list_of_clusters[cluster_association[i]].append(list_of_points[i])
        return list_of_clusters


