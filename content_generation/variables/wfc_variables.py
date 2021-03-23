from __future__ import annotations

from typing import List
from uuid import uuid4


class Tile:

    def __init__(self, nodes: List[tuple]):
        self.id: str = str(uuid4())
        self.nodes: List[tuple] = nodes
        self.neighbors: List[Tile] = []

    def add_neighbor(self, other: Tile):
        if other not in self.neighbors:
            self.neighbors.append(other)
        if self not in other.neighbors:
            other.neighbors.append(self)

    def print_neighbors(self):
        print("- - - - - - -")
        print(f"{self.id} has nodes:")
        print(self.nodes)
        print(f"and has the following neighbors:")
        for neighbor in self.neighbors:
            print(f"ID: {neighbor.id}")
            print(neighbor.nodes)
        print("- - - - - - -")

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.id[:8]}, Nodes:\n {self.nodes}>"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id is other.id

    def __ne__(self, other):
        return self.id is not other.id

    # def __deepcopy__(self, memodict={}):
    #     copy_object = 0


# def __deepcopy__(self, memo):
#     copy_object = SolutionArea(coordinates=self.list_of_coordinates, mass_coordinate=self.mass_coordinate,
#                                height=self.height, min_max_values=self.min_max_values,
#                                type_of_district=self.type_of_district)
#     return copy_object

# def __deepcopy__(self, memo):
#     copy_list = []
#     for x in self.population:
#         copy_list.append(copy.deepcopy(x, memo))
#     copy_object = SolutionGA(self.fitness, copy_list)
#     return copy_object

class Cluster:

    def __init__(self, tiles: List[Tile]):
        self.id: str = str(uuid4())
        self.tiles = tiles

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): ID {self.id[:8]}, Tile Count: {len(self.tiles)})"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id is other.id

    def __ne__(self, other):
        return self.id is not other.id
