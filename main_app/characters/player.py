from characters.base_character import BaseCharacter
# --- IMPORT CHANGE ---
from items_and_equipment.equipment import Equipment
from characters.race import Human, Elf, Dwarf, Orc, Halfling, Gnome, HalfElf # We import all races

class Player(BaseCharacter):
    """
    Represents the player character. Inherits from BaseCharacter and adds
    player-specific attributes like equipment, race, level-up system.
    """
    def __init__(self, name):
        super().__init__(name, level=1, attack_power=5, hit_points=20) # Starting stats
        self.experience = 0
        self.gold = 0
        self.equipment = Equipment()
        self.race = Human() # Default race
        self.unspent_attribute_points = 0 # Points to distribute on level up
        self.attribute_strength = 0 # Example attributes
        self.attribute_dexterity = 0
        self.attribute_intelligence = 0
        self.attribute_charisma = 0
        self.attribute_wisdom = 0
        self.attribute_constitution = 0
        self.inventory = [] # Player's inventory
        self.max_inventory_slots = 20  # Maximum number of items player can carry
        # Add some starter items for testing/demo
        from items_and_equipment.items import NarrowSword, LeatherArmor, BasicPotion, HealthPotion
        self.inventory.append(NarrowSword())
        self.inventory.append(LeatherArmor())
        self.inventory.append(BasicPotion())
        self.inventory.append(HealthPotion())

    def apply_race_bonuses(self):
        """Applies bonuses from the player's current race."""
        self.race.apply_bonuses(self)

    def gain_experience(self, amount):
        """
        Adds experience points to the player and checks for level-up.
        :param amount: Amount of experience to gain.
        """
        self.experience += amount
        self._check_for_level_up()

    def _check_for_level_up(self):
        """Checks if the player has enough experience to level up."""
        xp_to_next_level = self.level * 100 # Simple XP formula
        if self.experience >= xp_to_next_level:
            self.level_up()
            self.experience -= xp_to_next_level # Remaining XP carries over to the next level

    def level_up(self):
        """Increases player's level and attributes."""
        self.level += 1
        self._hit_points_max += 5 # Increase max HP
        self.hit_points = self._hit_points_max # Heal to full
        self.attack_power += 2 # Increase attack power
        self.unspent_attribute_points += 1 # Give a point to distribute

    def apply_item_bonus(self, item):
        """Applies bonuses from an equipped item. (Placeholder for now)"""
        # Here, logic that actually modifies the player's stats based on the item
        # e.g., self.attack_power += item.attack_bonus
        # Make sure the item has properties like attack_bonus
        if hasattr(item, 'attack_bonus'):
            self.attack_power += item.attack_bonus
        if hasattr(item, 'defense_bonus'):
            # We need a defense attribute in player.py
            pass # self.defense_power += item.defense_bonus
        pass

    def __str__(self):
        base_str = super().__str__()
        inventory_str = ", ".join(item.name for item in self.inventory) if self.inventory else "Empty"
        return (f"{base_str}\n"
                f"Race: {self.race.name}\n"
                f"XP: {self.experience}\n"
                f"Gold: {self.gold}\n"
                f"Unspent Attribute Points: {self.unspent_attribute_points}\n"
                f"Equipment: {self.equipment}\n"
                f"Strength: {self.attribute_strength}\n"
                f"Dexterity: {self.attribute_dexterity}\n"
                f"Intelligence: {self.attribute_intelligence}\n"
                f"Charisma: {self.attribute_charisma}\n"
                f"Wisdom: {self.attribute_wisdom}\n"
                f"Constitution: {self.attribute_constitution}\n"
                f"Inventory: {inventory_str} ({len(self.inventory)}/{self.max_inventory_slots})")