import multiprocessing

from map_analysis import MapAnalysis
from surface_builder import SurfaceBuilder
from shared_variables import SurfaceDictionaryValue
from minecraft_pb2 import Block
from map_variables import BOX_X_MIN, BOX_Z_MIN


class Deforest:
    __instance = None

    @staticmethod
    def getInstance():
        if Deforest.__instance is None:
            Deforest()
        return Deforest.__instance

    def __init__(self):
        if Deforest.__instance is not None:
            raise Exception("This is a singleton so don't initialize again")
        else:
            self.trees_for_persistence = {}
            self.surface_dict = {}
            self.block_dict = {}
            self.trees = [119, 120, 131, 132]
            self.full_trees = {}
            self.queue_for_removal = []
            self.tree_removal = []
            self.first_tree_x_y_z = []
            Deforest.__instance = self

    def __find_trees(self, list_clusters):
        for cluster in list_clusters[0]:
            for tile in cluster.tiles:
                for node in tile.nodes:
                    if node[0] >= BOX_X_MIN and node[1] >= BOX_Z_MIN:
                        if list_clusters[1][node[0], node[1]].block.type in self.trees:
                            self.trees_for_persistence[(node[0], node[1])] = list_clusters[1][node[0], node[1]].block

    def __read_tree(self):
        for tree in self.trees_for_persistence.keys():
            self.__tree_discovery(tree, self.surface_dict[tree].block.position.y)
        while self.queue_for_removal:
            node = self.queue_for_removal.pop()
            self.block_dict.update(MapAnalysis().read_part_of_world(node['min_x'], node['max_x'], node['min_z'],
                                                                    node['max_z'], True, node['min_y'], node['max_y'])[
                                       'block_dict'])

    def __tree_discovery(self, node, y):
        min_x, min_z = node[0] - 5, node[1] - 5
        max_x, max_z = node[0] + 5, node[1] + 5
        min_y, max_y = 0, 0
        global_min_z_in_surface_dict = min(self.surface_dict, key=lambda t: t[1])[1]
        global_min_x_in_surface_dict = min(self.surface_dict, key=lambda t: t[0])[0]
        if min_x >= global_min_x_in_surface_dict and min_z >= global_min_z_in_surface_dict:
            min_y = self.surface_dict[min_x, min_z].block.position.y - 5
            max_y = y + 5
        self.queue_for_removal.append({'min_x': min_x, 'min_z': min_z, 'min_y': min_y,
                                       'max_x': max_x, 'max_z': max_z, 'max_y': max_y})

    def __remove_trees(self):
        SurfaceBuilder().bulk_write_air(self.tree_removal)

    def __absolute_tree_finder(self):
        for node in self.block_dict:
            if self.block_dict[node]['type'] in self.trees:
                self.tree_removal.append(node)

    def rollback(self):
        temp_blocks = []
        for tree in self.tree_removal:
            random_block = Block()
            random_block.position.y = tree[1]
            random_block.position.x = tree[0]
            random_block.position.z = tree[2]
            random_block.type = self.block_dict[tree]['type']
            temp_blocks.append(random_block)
        SurfaceBuilder().spawn_blocks(temp_blocks)

    def __start_find_trees(self, data):
        with multiprocessing.Pool() as pool:
            pool.map(self.__find_trees, data)

    def run(self, clusters: list, surface_dict: dict):
        try:
            self.surface_dict = surface_dict
            data = [clusters, surface_dict]
            self.__find_trees(data)
            self.__read_tree()
            self.__absolute_tree_finder()
            self.__remove_trees()
            lis = sorted(self.block_dict.keys(), key=lambda t: t[1], reverse=True)

            for tree in self.trees_for_persistence.keys():
                templist = []
                for el in lis:
                    if el[0] == tree[0] and el[2] == tree[1]:
                        if not self.block_dict[el[0], el[1], el[2]]['type'] in [self.trees[2], self.trees[3], 5]:
                            templist.append(self.block_dict[el[0], el[1], el[2]])
                for ele in templist:
                    if ele['type'] in [self.trees[1], self.trees[0]]:
                        templist.remove(ele)
                templist = sorted(templist, key=lambda t: t['block'].position.y, reverse=True)
                tempconditionalvar = templist[0]['block'].position.y
                if (tree[0], tempconditionalvar, tree[1]) in self.block_dict:
                    heavy_sigh = SurfaceDictionaryValue(y=tempconditionalvar, block_type=
                    self.block_dict[tree[0], tempconditionalvar, tree[1]]['type'],
                                                        block=self.block_dict[tree[0], tempconditionalvar, tree[1]][
                                                            'block'])
                    surface_dict[tree[0], tree[1]] = heavy_sigh
        except:
            print("An exception occured. Rollback will commence.")
            self.rollback()
