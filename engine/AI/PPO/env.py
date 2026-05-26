import gymnasium as gym
from gymnasium import spaces
import numpy as np

from engine.game_engine import GameEngine
from engine.AI.PPO.rewards import RewardManager

class StrategyEnv(gym.Env):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.num_nodes = len(self.engine.map_manager.nodes)
        
        self.action_space = spaces.MultiDiscrete([self.num_nodes, self.num_nodes])
        
        self.obs_size = (self.num_nodes * 2) + (self.num_nodes * self.num_nodes)
        
        self.observation_space = spaces.Box(
            low=-1000, 
            high=1000, 
            shape=(self.obs_size,), 
            dtype=np.float32
        )

        self.ai_player = self.engine.players_manager.get_enemy_player()
        
        self.reward_manager = RewardManager()
        self.previous_node_states = {}
        self.previous_enemy_cp = 0

    def update_current_step(self, step: int):
        self.reward_manager.update_stage(step)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.engine = GameEngine(is_training=True, max_time=1000)
        self.engine.start()
        self.ai_player = self.engine.players_manager.get_enemy_player()
        
        self._save_state()
        
        return self._get_obs(), {}

    def step(self, action):
        source_id, target_id = action
        reward = 0
        
        if source_id == target_id:
            reward -= 0.05
        elif self._is_valid_action(source_id, target_id):
            self.engine.execute_action(source_id, target_id)
            reward += self.reward_manager.get_reward("valid_move")
        else:
            reward += self.reward_manager.get_reward("invalid_move")

        self.engine.update()
        
        reward += self._calculate_reward()
        
        obs = self._get_obs()
        terminated = self.engine.is_game_over() and not self.engine.is_time_out()
        truncated = self.engine.is_time_out()
        
        return obs, reward, terminated, truncated, {}

    def _get_obs(self):
        obs = np.zeros(self.obs_size, dtype=np.float32)
        
        for i, node in enumerate(self.engine.map_manager.nodes):
            owner_val = 0
            if node.owner == self.ai_player:
                owner_val = 1
            elif node.owner is not None:
                owner_val = -1
                
            obs[i * 2] = owner_val
            obs[i * 2 + 1] = node.combat_power
            
        offset = self.num_nodes * 2
        for i, node_a in enumerate(self.engine.map_manager.nodes):
            for j, node_b in enumerate(self.engine.map_manager.nodes):
                if node_b in node_a.connected_nodes:
                    obs[offset + (i * self.num_nodes) + j] = 1.0
                else:
                    obs[offset + (i * self.num_nodes) + j] = 0.0
                    
        return obs

    def _is_valid_action(self, source_id, target_id):
        nodes = self.engine.map_manager.nodes
        
        if source_id >= len(nodes) or target_id >= len(nodes):
            return False
            
        source_node = nodes[source_id]
        target_node = nodes[target_id]
        
        if source_node.owner != self.ai_player:
            return False
            
        if source_node.combat_power <= 0:
            return False
            
        if target_node not in source_node.connected_nodes:
            return False
            
        return True

    def _save_state(self):
        self.previous_node_states = {}
        enemy_cp = 0
        
        for node in self.engine.map_manager.nodes:
            self.previous_node_states[node.id] = node.owner
            if node.owner is not None and node.owner != self.ai_player:
                enemy_cp += node.combat_power
                
        self.previous_enemy_cp = enemy_cp

    def _calculate_reward(self):
        reward = 0
        current_enemy_cp = 0
        
        for node in self.engine.map_manager.nodes:
            prev_owner = self.previous_node_states[node.id]
            curr_owner = node.owner
            
            if curr_owner is not None and curr_owner != self.ai_player:
                current_enemy_cp += node.combat_power

            if curr_owner == self.ai_player and prev_owner != self.ai_player:
                if prev_owner is None:
                    reward += self.reward_manager.get_reward("capture_empty")
                else:
                    reward += self.reward_manager.get_reward("capture_enemy")
                        
            elif prev_owner == self.ai_player and curr_owner != self.ai_player:
                reward += self.reward_manager.get_reward("lose_node")

        enemy_cp_diff = self.previous_enemy_cp - current_enemy_cp
        if enemy_cp_diff > 0:
            reward += enemy_cp_diff * self.reward_manager.get_reward("enemy_cp_diff_mult")
                
        if self.engine.is_game_over():
            if self.engine.is_time_out():
                reward += self.reward_manager.get_reward("time_out")
            else:
                has_nodes = any(node.owner == self.ai_player for node in self.engine.map_manager.nodes)
                if has_nodes:
                    reward += self.reward_manager.get_reward("win_game")
                else:
                    reward += self.reward_manager.get_reward("lose_game")

        self._save_state()
        return reward

    def render(self):
        print("\n--- STAN MAPY ---")
        for node in self.engine.map_manager.nodes:
            owner = node.owner.name if node.owner else "None"
            print(f"Node {node.id} | Owner: {owner} | CP: {int(node.combat_power)}")