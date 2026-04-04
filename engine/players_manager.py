import random
from pygame import Color

from engine.player import Player
from engine.node import Node
from engine.AI.random_actions import AIController
from engine.game_actions import ActionsManager
from engine.map_manager import MapManager

class PlayersManager:
    def __init__(self, player_count: int, map_manager: MapManager, local_player: bool = False):
        self.player_count = player_count
        self.players = []
        self.map_manager = map_manager

    def init(self, actions_manager: ActionsManager):
        self.players = self.create_players()
        self.spawn_players(self.map_manager.nodes)
        self.add_controller_for_players(actions_manager)

    def create_players(self) -> list[Player]:
        return [
            Player(f"Bot {index}", Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), False) for index in range(self.player_count)
        ]
    
    def add_controller_for_players(self, actions_manager: ActionsManager):
        for player in self.players:
            player.controller = AIController(player, actions_manager, self.map_manager)
    
    def spawn_players(self, nodes: list[Node]):
        spawned_players_count = 0
        while spawned_players_count < self.player_count:
            node = random.choice(nodes)
            if node.owner is None:
                node.owner = self.players[spawned_players_count]
                spawned_players_count += 1
    
    def get_active_players(self) -> list[Player]:
        return [player for player in self.players if len(self.map_manager.get_nodes_owned_by_player(player)) > 0]