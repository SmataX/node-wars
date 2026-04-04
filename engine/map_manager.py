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

    def get_node_by_id(self, id: int) -> Node:
        return self.nodes[id]
    
    def get_nodes_owned_by_player(self, player: Player) -> list[Node]:
        return [node for node in self.nodes if node.owner is player]