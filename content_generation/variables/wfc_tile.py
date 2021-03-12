from typing import List
from uuid import uuid4


class Tile:

    def __init__(self, nodes: List[tuple], neighbors: List):
        self.id: str = str(uuid4())
        self.nodes: List[tuple] = nodes
        self.neighbor: List[Tile] = neighbors

    def __repr__(self):
        return f"<{self.__class__.__name__} ({hex(id(self))}): {self.id[:8]}, Nodes:\n {self.nodes}>"

