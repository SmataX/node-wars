import random
import math
from engine.node import Node
from engine.vector import Vector
from scipy.spatial import Delaunay


class MapGenerator:

    @staticmethod
    def generate(node_count: int) -> list[Node]:
        nodes = MapGenerator.generate_nodes(node_count)
        MapGenerator.generate_connections(nodes)

        return nodes
    
    @staticmethod
    def generate_nodes(node_count: int) -> list[Node]:
        nodes: list[Node] = []
        index = 0
        while node_count > 0:
            random_position = Vector(random.randint(0, 100), random.randint(0, 100))

            temp = True
            for node in nodes:
                if Vector.distance(random_position, node.position) < 1:
                    temp = False
                    break

            if temp:
                nodes.append(Node(index, random_position, connected_nodes=[]))
                index += 1
                node_count -= 1
        
        return nodes

    @staticmethod
    def generate_connections(nodes: list[Node]):
        points = [[n.position.x, n.position.y] for n in nodes]
        
        tri = Delaunay(points)

        for simplex in tri.simplices:
            for i in range(3):
                node_a = nodes[simplex[i]]
                node_b = nodes[simplex[(i + 1) % 3]]

                if node_b not in node_a.connected_nodes:
                    node_a.connected_nodes.append(node_b)
                if node_a not in node_b.connected_nodes:
                    node_b.connected_nodes.append(node_a)