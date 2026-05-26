STAGES_CONFIG = {
    1: {
        "name": "Eksploracja",
        "start_step": 0,
        "rewards": {
            "valid_move": 0.5,
            "invalid_move": -0.5,
            "capture_empty": 0.0,
            "capture_enemy": 0.0,
            "lose_node": 0.0,
            "win_game": 0.0,
            "lose_game": 0.0,
            "time_out": 0.0,
            "enemy_cp_diff_mult": 0.0
        }
    },
    2: {
        "name": "Ekspansja",
        "start_step": 500_000,
        "rewards": {
            "valid_move": 0.0,
            "invalid_move": -0.1,
            "capture_empty": 10.0,
            "capture_enemy": 0.0,
            "lose_node": 0.0,
            "win_game": 0.0,
            "lose_game": 0.0,
            "time_out": 0.0,
            "enemy_cp_diff_mult": 0.0
        }
    },
    3: {
        "name": "Dominacja",
        "start_step": 1_500_000,
        "rewards": {
            "valid_move": 0.0,
            "invalid_move": -0.1,
            "capture_empty": 12.0,
            "capture_enemy": 25.0,
            "lose_node": -10.0,
            "win_game": 200.0,
            "lose_game": -100.0,
            "time_out": -50.0,
            "enemy_cp_diff_mult": 0.1
        }
    }
}

class RewardManager:
    def __init__(self):
        self.current_stage = 1

    def update_stage(self, current_step: int) -> int:
        for stage_num in sorted(STAGES_CONFIG.keys(), reverse=True):
            if current_step >= STAGES_CONFIG[stage_num]["start_step"]:
                self.current_stage = stage_num
                break
        return self.current_stage

    def get_reward(self, event: str) -> float:
        return STAGES_CONFIG[self.current_stage]["rewards"].get(event, 0.0)