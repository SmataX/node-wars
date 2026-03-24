import random
from node import Node
from vector import Vector


class MapGenerator:
    def generate(node_count: int) -> list[Node]:
        nodes = []
        for i in range(node_count):
            nodes.append(
                Node(i, Vector(random.randint(0, 100), random.randint(0, 100)), [])
            )

        return nodes