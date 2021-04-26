DISALLOWED_Y_DIFFERENCE = {1, 2}


class APoint:

    def __init__(self, node: tuple, y: int):
        self.node = node
        self.y = y

    def __eq__(self, other):
        if self.node == other.node:
            if self.y == -1 or other.y == -1:
                return True
            return self.y == other.y
        else:
            return False

    def __hash__(self):
        return hash((self.node[0], self.node[1], self.y))

    def __repr__(self):
        return f"<node:{self.node}, y:{self.y}>"

    def __lt__(self, other):
        return self.node < other.node

    def __le__(self, other):
        return self.node <= other.node
