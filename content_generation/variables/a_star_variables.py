from uuid import uuid4


class APoint:

    def __init__(self, node: tuple, y: int):
        self.node = node
        self.y = y
        self.id: str = str(uuid4())

    def __eq__(self, other):
        if self.node == other.node:
            if self.y == -1 or other.y == -1:
                return True
            return self.y == other.y
        else:
            return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<node:{self.node}, y:{self.y}>"

    def __lt__(self, other):
        return self.node < other.node

    def __le__(self, other):
        return self.node <= other.node
