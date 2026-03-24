from node import Node
from map_generator import MapGenerator

class MapManager:
    def __init__(self, node_count):
        self.node_count = node_count
        self.nodes = list()
    
    def init(self):
        self.nodes = MapGenerator.generate(self.node_count)