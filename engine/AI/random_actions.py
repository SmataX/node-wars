from engine.game_actions import ActionsManager
from engine.map_manager import MapManager
from engine.player import Player

import random

class AIController:
    def __init__(self, player: Player, actions_manager: ActionsManager, map_manager: MapManager):
        self.player = player
        self.actions_manager = actions_manager
        self.map_manager = map_manager

    def make_random_action(self):
        random_node = random.choice(self.player.owned_nodes)
        random_connected_node = random.choice(random_node.connected_nodes)

        self.actions_manager.move(random_node.id, random_connected_node.id, self.player)