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
        print(f"{self.id} is neighbor to:")
        print(self.nodes)
        print("- - - - - - -")
        for neighbor in self.neighbors:
            print(f"ID: {neighbor.id}")
            print(neighbor.nodes)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.id[:8]}, Nodes:\n {self.nodes}>"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id is other.id

    def __ne__(self, other):
        return self.id is not other.id
