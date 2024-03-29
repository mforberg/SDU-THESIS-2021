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
        self.district_type = "Nothing"
        self.states: List[State] = []
        self.entropy = 0  # reassigned later

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

    def assign_states(self, states: List[State]):
        self.states = states
        sum_of_weights = 0
        pp_weights = 0
        for state in self.states:
            sum_of_weights += state.weight
            pp_weights += state.weight * log(state.weight)
        entropy = (log(sum_of_weights) - pp_weights / sum_of_weights)
        noise = random.uniform(0, (entropy*0.05))
        self.entropy = entropy - noise

    def update_entropy(self):
        sum_of_weights = 0
        pp_weights = 0
        for state in self.states:
            sum_of_weights += state.weight
            pp_weights += state.weight * log(state.weight)
        self.entropy = (log(sum_of_weights) - pp_weights / sum_of_weights)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): ID[:8] {self.id[:8]}, CA: {self.cluster_assignment}, Nodes: {self.nodes}, Neighbors: {len(self.neighbors)}, State: {self.states}> \n"

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

    def __init__(self, state_type: str, pattern, legal_neighbors, needs: List[str]):
        self.state_type = state_type
        self.pattern = pattern
        self.legal_neighbors = legal_neighbors # {neighbor: str = [valid_dir: str, valid_dir: str]
        self.weight = 1  # reassigned later
        self.needs = needs

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): TYPE={self.state_type}, WEIGHT={self.weight}, needs={self.needs}>"

    def __eq__(self, other):
        return self.state_type == other.state_type

    def __hash__(self):
        return hash(self.state_type)


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
