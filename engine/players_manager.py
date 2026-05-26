import random
from typing import TYPE_CHECKING
from pygame import Color

from engine.player import Player
from engine.node import Node
from engine.AI.ppo_controller import PPOController
from engine.AI.random_actions import AIController

class PlayersManager:
    def __init__(self, player_count: int):
        self.player_count = player_count
        self.players = []
        self.active_players = []
        self.engine = None

    def init(self, engine):
        self.engine = engine
        self.players = self.create_players()
        self.active_players = self.players.copy()
        self.spawn_players()

    def create_players(self) -> list[Player]:
        players = []
        for index in range(self.player_count):
            color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            player = Player(f"Bot {index}", color, controller=None)
            
            if self.engine.is_training:
                player.controller = AIController(player, self.engine.actions_manager, self.engine.map_manager)
            else:
                try:
                    player.controller = PPOController(player, self.engine.actions_manager, self.engine.map_manager, "ppo_bot")
                except Exception:
                    player.controller = AIController(player, self.engine.actions_manager, self.engine.map_manager)
                    
            players.append(player)
        return players
    
    def spawn_players(self):
        nodes_source = self.engine.map_manager.nodes
        all_nodes = list(nodes_source.values()) if isinstance(nodes_source, dict) else nodes_source
        
        random_nodes = random.sample(all_nodes, self.player_count)
        for player, node in zip(self.players, random_nodes):
            node.owner = player
            player.owned_nodes.append(node)

    def get_enemy_player(self) -> Player:
        return self.players[0] if self.players else None