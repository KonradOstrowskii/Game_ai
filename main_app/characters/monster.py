from .base_character import BaseCharacter

class Monster(BaseCharacter):
    """
    Represents a monster in the game. Inherits from BaseCharacter.
    """
    def __init__(self, name, level, attack_power, hit_points, experience_reward=10, treasure_reward=1):
        super().__init__(name, level, attack_power, hit_points)
        self.experience_reward = experience_reward
        self.treasure_reward = treasure_reward # Number of treasures/cards to gain

    # Monster-specific methods can be added, e.g., special attacks, resistances
    def __str__(self):
        return (f"Monster: {self.name}\n"
                f"Level: {self.level}\n"
                f"Attack: {self.attack_power}\n"
                f"HP: {self.hit_points}/{self._hit_points_max}\n"
                f"XP Reward: {self.experience_reward}")