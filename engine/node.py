from engine.vector import Vector

class Node:
    def __init__(self, id: int, position: Vector, connected_nodes: list["Node"]):
        self.id = id
        self.position = position
        self.connected_nodes = connected_nodes
        
        self.owner = None
        self.combat_power = 0
        self.combat_power_income = 1
        
