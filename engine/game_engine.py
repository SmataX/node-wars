from engine.map_manager import MapManager
from engine.players_manager import PlayersManager

class GameEngine:
    def __init__(self, node_count: int = 10, player_count: int = 3):
        self.map_manager = MapManager(node_count)
        self.players_manager = PlayersManager(player_count)

    def start(self):
        print("[info] Start")
        self.map_manager.init()
        self.players_manager.init(self.map_manager.nodes)


if __name__ == "__main__":
    engine = GameEngine()
    engine.start()