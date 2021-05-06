from __future__ import annotations
from typing import List
from uuid import uuid4
from math import log
import random


class Tile:

    def __init__(self, nodes: List[tuple]):
        self.id: str = str(uuid4())
        self.nodes: List[tuple] = nodes
        self.neighbors: List[Tile] = []
        self.cluster_assignment = -1  # Reassigned later
        self.collapsed = False
        self.type_of_tile = "Nothing"
        self.states: [State] = []
        self.entropy = 0  # TODO: Implement something to assign this + figure out how to calc this

    def add_neighbor(self, other: Tile):
        if other not in self.neighbors:
            self.neighbors.append(other)
        if self not in other.neighbors:
            other.neighbors.append(self)

    def remove_neighbor(self, other: Tile):
        if other in self.neighbors:
            self.neighbors.remove(other)
        if self in other.neighbors:
            other.neighbors.remove(self)

    def print_neighbors(self):
        print("- - - - - - -")
        print(f"{self.id} has nodes:")
        print(self.nodes)
        print(f"and has the following neighbors:")
        for neighbor in self.neighbors:
            print(f"ID: {neighbor.id}")
            print(neighbor.nodes)
        print("- - - - - - -")

    def assign_states(self, states: [State]):
        self.states = states
        sum_of_weights = 0
        pp_weights = 0
        for state in self.states:
            sum_of_weights += state.weight
            pp_weights += state.weight * log(state.weight)
        entropy = (log(sum_of_weights) - pp_weights / sum_of_weights)
        noise = random.uniform(0, (entropy*0.05))
        self.entropy = entropy - noise
        # print("- - - - look here - - - - -")
        # print(f"entropy: {entropy}, noise: {noise}")
        # print(self.entropy)

    def update_entropy(self):
        sum_of_weights = 0
        pp_weights = 0
        for state in self.states:
            sum_of_weights += state.weight
            pp_weights += state.weight * log(state.weight)
        self.entropy = (log(sum_of_weights) - pp_weights / sum_of_weights)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): ID[:8] {self.id[:8]}, CA: {self.cluster_assignment}, Nodes:\n {self.nodes}>"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __lt__(self, other):
        return self.entropy < other.entropy

    def __le__(self, other):
        return self.entropy <= other.entropy


class State:

    def __init__(self, state_type: str, pattern, legal_neighbors: [str]):
        self.type = state_type
        self.pattern = pattern
        self.legal_neighbors = legal_neighbors
        self.weight = 1  # reassigned later

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}: TYPE={self.type}, WEIGHT={self.weight}>"

    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)


class Pattern:

    def __init__(self, pattern):
        self.pattern = pattern


class Cluster:

    def __init__(self, tiles: List[Tile]):
        self.id: str = str(uuid4())
        self.tiles = tiles
        self.y = -1  # Changed later

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): ID {self.id[:8]}, Tile Count: {len(self.tiles)})>"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id is other.id

    def __ne__(self, other):
        return self.id is not other.id
