from map_manager import MapManager

class GameEngine:
    def __init__(self, node_count: int = 10):
        self.map_manager = MapManager(node_count)

    def start(self):
        print("[info] Start")
        self.map_manager.init()


if __name__ == "__main__":
    engine = GameEngine()
    engine.start()