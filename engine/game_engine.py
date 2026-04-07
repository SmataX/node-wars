import time

from engine.map_manager import MapManager
from engine.players_manager import PlayersManager
from engine.game_actions import ActionsManager

class GameEngine:
    def __init__(self, node_count: int = 10, player_count: int = 3):
        self.map_manager = MapManager(node_count)
        self.players_manager = PlayersManager(player_count, self.map_manager)
        self.actions_manager = ActionsManager(self.map_manager, self.players_manager)
        
        self.timer = 0
        self.last_time = time.time()

    def start(self):
        print("[info] Start")
        self.map_manager.init()
        self.players_manager.init(self.actions_manager)

    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        self.timer += dt

        if self.timer >= 1.0:
            print("[info] Update")
            self.map_manager.update()
            self.timer = 0

            for player in self.players_manager.active_players:
                player.controller.make_random_action()

        if len(self.players_manager.active_players) == 1:
            print(f"[INFO] {self.players_manager.active_players[0].name} wins a game")


if __name__ == "__main__":
    engine = GameEngine()
    engine.start()