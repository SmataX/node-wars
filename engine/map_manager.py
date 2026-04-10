from engine.node import Node
from engine.map_generator import MapGenerator
from engine.player import Player

class MapManager:
    def __init__(self, node_count):
        self.node_count = node_count
        self.nodes = list()
    
    def init(self):
        self.nodes = MapGenerator.generate(self.node_count)

    def update(self):
        for node in self.nodes:
            node.increase_combat_power()