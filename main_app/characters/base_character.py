import math

class BaseCharacter:
    """
    Base class for all characters in the game, including player and monsters.
    Defines core attributes and combat mechanics.
    """
    def __init__(self, name, level, attack_power, hit_points):
        self.name = name
        self.level = level
        self._attack_power = attack_power
        self._hit_points_max = hit_points
        self._hit_points = hit_points
        self.alive = True
        self._damage = 0 # Last damage dealt, used for display in the log

    @property
    def attack_power(self):
        """Getter for attack_power."""
        return self._attack_power

    @attack_power.setter
    def attack_power(self, value):
        """Setter for attack_power, ensures it's not negative."""
        self._attack_power = max(0, value)

    @property
    def hit_points(self):
        """Getter for hit_points."""
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        """Setter for hit_points, updates alive status and caps at max HP."""
        self._hit_points = max(0, min(value, self._hit_points_max))
        self.alive = self._hit_points > 0

    def take_damage(self, amount):
        """
        Reduces character's hit points by the given amount.
        Handles defensive racial skills (Dodge, Block).
        
        Damage reduction priority:
        1. Dodge skill - completely avoids damage
        2. Block skill - reduces damage by 50%
        3. Normal - takes full damage
        
        :param amount: Amount of damage to take.
        """
        final_damage = self._apply_defensive_skills(amount)
        
        # Apply the calculated damage
        if final_damage > 0:
            self.hit_points -= final_damage

    def _apply_defensive_skills(self, damage_amount):
        """
        Applies defensive racial skills to reduce or avoid damage.
        Returns the final damage amount after skill application.
        
        :param damage_amount: The incoming damage amount.
        :return: Final damage after skill reduction (0 if dodged/blocked).
        """
        # Only player characters have races with skills
        if not hasattr(self, 'race') or not self.race:
            return damage_amount
        
        # Priority 1: Dodge (complete avoidance)
        if 'Dodge' in self.race.skills:
            dodge_func = self.race.skills['Dodge']
            if dodge_func() is True:
                return 0  # Damage completely avoided
        
        # Priority 2: Block (damage reduction), only if dodge failed
        if 'Block' in self.race.skills:
            block_func = self.race.skills['Block']
            if block_func() is True:
                # 50% damage reduction on successful block
                return math.ceil(damage_amount * 0.5)
        
        # No skills triggered - take full damage
        return damage_amount 

    def attack(self, target):
        """
        Performs an attack on a target character.
        :param target: The target BaseCharacter to attack.
        """
        if not self.alive:
            return

        damage_dealt = self._calculate_damage()
        target.take_damage(damage_dealt)
        self._damage = damage_dealt # Save the damage dealt

    def _calculate_damage(self):
        """
        Calculates the actual damage dealt, applying offensive racial skills (Berserk).
        :return: Calculated damage amount.
        """
        damage = self.attack_power
        
        # --- OFFENSIVE SKILLS LOGIC (Berserk) ---
        # We check if the object has a race (applies to the player) and if it has an active Berserk
        if hasattr(self, 'race') and self.race:
            if 'Berserk' in self.race.skills:
                berserk_func = self.race.skills['Berserk']
                if berserk_func() is True:
                    # 50% damage increase
                    damage = math.ceil(damage * 1.5)
                    print(f"!!! {self.name}'s Battle Fury (Berserk) is active! Damage increased to {damage} !!!")
            
            # --- NEW: ADRENALINE RUSH LOGIC ---
            if 'Adrenaline Rush' in self.race.skills:
                # Check if HP is below 25%
                if self.hit_points < (self._hit_points_max * 0.25):
                    adrenaline_func = self.race.skills['Adrenaline Rush']
                    if adrenaline_func():
                        # 75% damage increase
                        damage = math.ceil(damage * 1.75)
                        print(f"!!! {self.name}'s Adrenaline Rush is active! Damage increased to {damage} !!!")

        # Simple implementation, just attack power. Can be expanded with modifiers.
        return damage

    def heal(self, amount):
        """
        Heals the character, increasing hit points up to max.
        :param amount: Amount of hit points to restore.
        """
        if not self.alive:
            print(f"{self.name} is defeated and cannot be healed this way.")
            return
        self.hit_points += amount
        print(f"{self.name} healed for {amount} HP. Current HP: {self.hit_points}")

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Level: {self.level}\n"
                f"Attack: {self._attack_power}\n"
                f"HP: {self._hit_points}/{self._hit_points_max}")