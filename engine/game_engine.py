import time
from engine.map_manager import MapManager
from engine.players_manager import PlayersManager
from engine.game_actions import ActionsManager

class GameEngine:
    def __init__(self, node_count: int = 10, player_count: int = 3, is_training: bool = False, max_time: int = 1000):
        self.map_manager = MapManager(node_count)
        self.players_manager = PlayersManager(player_count)
        self.actions_manager = ActionsManager(self.map_manager, self.players_manager)
        
        self.is_training = is_training
        self.timer = 0
        self.last_time = time.time()
        
        self.max_time = max_time
        self.elapsed_time = 0

    def start(self):
        # print("[info] Start")
        self.map_manager.init()
        self.players_manager.init(engine=self)

    def update(self):
        if self.is_training:
            dt = 1.0 
        else:
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time

        self.timer += dt

        if self.timer >= 1.0 or self.is_training: 
            self.elapsed_time += 1
            self.map_manager.update()
            if not self.is_training:
                self.timer = 0 

            for player in self.players_manager.active_players[:]: 
                if len(player.owned_nodes) == 0:
                    # print(f"[INFO] {player.name} lost a game!")
                    self.players_manager.active_players.remove(player)

            ai_player = self.players_manager.get_enemy_player()
            for player in self.players_manager.active_players:
                if len(player.owned_nodes) > 0:
                    if not self.is_training or player != ai_player:
                        if player.controller:
                            player.controller.make_action()

        if self.is_game_over():
            if len(self.players_manager.active_players) == 1:
                print(f"[INFO] {self.players_manager.active_players[0].name} wins a game")
            elif self.is_time_out():
                print("[INFO] Time limit reached!")
            return False
            
        return True
    
    def execute_action(self, source_id, target_id):
        ai_player = self.players_manager.get_enemy_player() 
        self.actions_manager.move(source_id, target_id, ai_player)

    def is_time_out(self) -> bool:
        return self.elapsed_time >= self.max_time

    def is_game_over(self) -> bool:
        return len(self.players_manager.active_players) <= 1 or self.is_time_out()