import numpy as np
import random
from stable_baselines3 import PPO

class PPOController:
    def __init__(self, player, actions_manager, map_manager, model_path="ppo_bot"):
        self.player = player
        self.actions_manager = actions_manager
        self.map_manager = map_manager
        self.model = PPO.load(model_path)

    def _get_obs(self):
        nodes = self.map_manager.nodes
        num_nodes = len(nodes)
        obs_size = (num_nodes * 2) + (num_nodes * num_nodes)
        obs = np.zeros(obs_size, dtype=np.float32)
        
        for i, node in enumerate(nodes):
            owner_val = 0
            if node.owner == self.player:
                owner_val = 1
            elif node.owner is not None:
                owner_val = -1
                
            obs[i * 2] = owner_val
            obs[i * 2 + 1] = node.combat_power
            
        offset = num_nodes * 2
        for i, node_a in enumerate(nodes):
            for j, node_b in enumerate(nodes):
                if node_b in node_a.connected_nodes:
                    obs[offset + (i * num_nodes) + j] = 1.0
                else:
                    obs[offset + (i * num_nodes) + j] = 0.0
            
        return obs

    def make_action(self):
        obs = self._get_obs()
        action, _states = self.model.predict(obs, deterministic=True)
        source_id, target_id = action
        
        nodes = self.map_manager.nodes
        action_executed = False
        
        if source_id < len(nodes) and target_id < len(nodes):
            if source_id == target_id:
                action_executed = True
            else:
                source_node = nodes[source_id]
                target_node = nodes[target_id]
                
                if source_node.owner == self.player and source_node.combat_power > 0:
                    if target_node in source_node.connected_nodes:
                        self.actions_manager.move(source_id, target_id, self.player)
                        action_executed = True
                    
        if not action_executed:
            self._make_fallback_action()

    def _make_fallback_action(self):
        if not self.player.owned_nodes:
            return
            
        random_node = random.choice(self.player.owned_nodes)
        
        if not random_node.connected_nodes:
            return
            
        random_connected_node = random.choice(random_node.connected_nodes)
        self.actions_manager.move(random_node.id, random_connected_node.id, self.player)