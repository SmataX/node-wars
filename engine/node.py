from engine.vector import Vector
from engine.player import Player

class Node:
    def __init__(self, id: int, position: Vector, connected_nodes: list["Node"], combat_power: int = 10):
        self.id = id
        self.position = position
        self.connected_nodes = connected_nodes
        
        self.owner = None
        self.combat_power = combat_power
        self.combat_power_income = 1

    def increase_combat_power(self):
        if self.combat_power < 500 and self.owner is not None:
            self.combat_power += self.combat_power_income

    def capture_node(self, player: Player, new_cp: int):
        if self.owner is not None:
            self.owner.owned_nodes.remove(self)

        self.owner = player
        self.combat_power = new_cp
        self.owner.owned_nodes.append(self)
        
