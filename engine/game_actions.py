from engine.map_manager import MapManager
from engine.player import Player

class ActionsManager:
    def __init__(self, map_manager: MapManager, players_manager):
        self.map_manager = map_manager
        self.players_manager = players_manager

    def move(self, node_id: int, target_node_id: int, player: Player):
        node = self.map_manager.nodes[node_id]
        target_node = self.map_manager.nodes[target_node_id]

        if node.owner is not player:
            return
        
        if node.owner == target_node.owner:
            cp_to_move = node.combat_power if node.combat_power + target_node.combat_power <= 500 else 500 - target_node.combat_power
            node.combat_power -= cp_to_move
            target_node.combat_power += cp_to_move
            print(f"[INFO] {player.name} is moving from {node_id} to {target_node_id}")

        else:
            if node.combat_power > target_node.combat_power:
                remaining_cp = node.combat_power - target_node.combat_power
                target_node.capture_node(player, remaining_cp)
                node.combat_power = 0
                print(f"[INFO] {player.name} captured {target_node_id}!")
            else:
                target_node.combat_power -= node.combat_power
                node.combat_power = 0
                print(f"[INFO] {player.name} attack on {target_node_id} failed. Units lost.")

