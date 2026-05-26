import random
import numpy as np
from stable_baselines3 import PPO

class AIController:
    def __init__(self, player, actions_manager, map_manager, model_path=None):
        self.player = player
        self.actions_manager = actions_manager
        self.map_manager = map_manager
        self.model = PPO.load(model_path) if model_path else None

    def _get_observation(self):
        nodes = self.map_manager.nodes
        obs = np.zeros(len(nodes) * 2, dtype=np.float32)
        
        for i, node in enumerate(nodes):
            owner_val = 0
            if node.owner == self.player:
                owner_val = 1
            elif node.owner is not None:
                owner_val = -1
                
            obs[i * 2] = owner_val
            obs[i * 2 + 1] = node.combat_power
            
        return obs

    def make_action(self):
        if not self.model:
            self._make_random_action()
            return

        obs = self._get_observation()
        action, _states = self.model.predict(obs, deterministic=True)
        
        source_idx, target_idx, action_type = action
        nodes = self.map_manager.nodes
        
        if source_idx < len(nodes) and target_idx < len(nodes):
            source_node = nodes[source_idx]
            target_node = nodes[target_idx]
            
            self._execute_predicted_action(source_node.id, target_node.id, action_type)

    def _execute_predicted_action(self, source_id, target_id, action_type):
        self.actions_manager.move(source_id, target_id, self.player)

    def _make_random_action(self):
        if not self.player.owned_nodes:
            return
            
        random_node = random.choice(self.player.owned_nodes)
        
        if not random_node.connected_nodes:
            return
            
        random_connected_node = random.choice(random_node.connected_nodes)
        self.actions_manager.move(random_node.id, random_connected_node.id, self.player)