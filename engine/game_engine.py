import time

from engine.map_manager import MapManager
from engine.players_manager import PlayersManager

class GameEngine:
    def __init__(self, node_count: int = 10, player_count: int = 3):
        self.map_manager = MapManager(node_count)
        self.players_manager = PlayersManager(player_count)
        
        self.timer = 0
        self.last_time = time.time()

    def start(self):
        print("[info] Start")
        self.map_manager.init()
        self.players_manager.init(self.map_manager.nodes)

    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        self.timer += dt

        if self.timer >= 1.0:
            self.map_manager.update()
            self.timer = 0


if __name__ == "__main__":
    engine = GameEngine()
    engine.start()