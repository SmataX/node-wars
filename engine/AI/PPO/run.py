import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor

from engine.AI.PPO.env import StrategyEnv
from engine.game_engine import GameEngine

class CurriculumCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        self.training_env.env_method("update_current_step", self.num_timesteps)
        
        current_stage = self.training_env.get_attr("reward_manager")[0].current_stage
        self.logger.record('curriculum/stage', current_stage)
        
        return True

LOAD_PREVIOUS_MODEL = True
MODEL_PATH = "ppo_bot"
LOG_DIR = "./ppo_logs/" 

os.makedirs(LOG_DIR, exist_ok=True)

engine = GameEngine(is_training=True)
engine.start()

env = Monitor(StrategyEnv(engine), filename=os.path.join(LOG_DIR, "training_data"))
check_env(env)

if LOAD_PREVIOUS_MODEL and os.path.exists(f"{MODEL_PATH}.zip"):
    print(f"[INFO] Wczytywanie poprzedniego modelu: {MODEL_PATH}")
    model = PPO.load(MODEL_PATH, env=env, tensorboard_log=LOG_DIR, verbose=1)
else:
    print("[INFO] Tworzenie nowego modelu od zera")
    policy_kwargs = dict(net_arch=dict(pi=[256, 256, 256], vf=[256, 256, 256]))
model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, tensorboard_log=LOG_DIR, verbose=1)

callback = CurriculumCallback()

model.learn(total_timesteps=10_000_000, callback=callback, reset_num_timesteps=False)

model.save(MODEL_PATH)