import random
from pygame import Color

from engine.player import Player
from engine.node import Node

class PlayersManager:
    def __init__(self, player_count: int, local_player: bool = False):
        self.player_count = player_count
        self.players = []

    def init(self, nodes: list[Node]):
        self.players = self.create_players()
        self.spawn_players(nodes)

    def create_players(self) -> list[Player]:
        return [
            Player(f"Bot {index}", Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), False) for index in range(self.player_count)
        ]
    
    def spawn_players(self, nodes: list[Node]):
        spawned_players_count = 0
        while spawned_players_count < self.player_count:
            node = random.choice(nodes)
            if node.owner is None:
                node.owner = self.players[spawned_players_count]
                spawned_players_count += 1
    
    def get_active_players(self) -> list[Player]:
        pass