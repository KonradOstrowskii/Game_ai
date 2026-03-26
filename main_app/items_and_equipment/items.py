class Item:
    """Base class for all items in the game."""
    def __init__(self, name, description, item_type="general", attack_bonus=0, defense_bonus=0, gold_value=0):
        self.name = name
        self.description = description
        self.item_type = item_type # e.g., "weapon", "armor", "potion", "general"
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.gold_value = gold_value

    def __str__(self):
        return f"{self.name} ({self.item_type}): {self.description}"

class Weapon(Item):
    """Specific class for weapons."""
    def __init__(self, name, attack_bonus, description="A standard weapon.", gold_value=5):
        super().__init__(name, description, "weapon", attack_bonus=attack_bonus, gold_value=gold_value)

class Armor(Item):
    """Specific class for armor."""
    def __init__(self, name, defense_bonus, description="Standard armor.", gold_value=5):
        super().__init__(name, description, "armor", defense_bonus=defense_bonus, gold_value=gold_value)

# --- Example items ---
class NarrowSword(Weapon):
    def __init__(self):
        super().__init__("Narrow Sword", 3, "A slim, elegant blade favoured by Elves.")

class BigStick(Weapon):
    def __init__(self):
        super().__init__("Big Stick", 4, "A surprisingly effective large stick, favoured by Orcs.")

class LeatherArmor(Armor):
    def __init__(self):
        super().__init__("Leather Armor", 2, "Light leather armor.")

class BasicPotion(Item):
    def __init__(self):
        super().__init__("Basic Potion", "Restores a small amount of health.", item_type="potion", gold_value=2)

# --- More Items ---
class StrengthPotion(Item):
    """A potion that temporarily boosts strength."""
    def __init__(self):
        super().__init__("Strength Potion", "Temporarily boosts your attack power for one fight.", item_type="potion", gold_value=15)

class RustySword(Weapon):
    def __init__(self):
        super().__init__("Rusty Sword", 2, "A sword that has seen better days.", gold_value=3)

class IronHelmet(Armor):
    def __init__(self):
        # Note: Currently, only one piece of armor can be equipped. This would replace the body armor.
        # A more complex system would have separate slots (head, chest, etc.).
        super().__init__("Iron Helmet", 1, "A sturdy iron helmet. Better than nothing.", 10)

# --- Even More Items for Loot Pool ---
class HealthPotion(Item):
    def __init__(self):
        super().__init__("Health Potion", "Restores 10 HP.", item_type="potion", gold_value=10)

class ManaPotion(Item):
    def __init__(self):
        super().__init__("Mana Potion", "Restores 10 MP.", item_type="potion", gold_value=12)

class MithrilChainmail(Armor):
    def __init__(self):
        super().__init__("Mithril Chainmail", 4, "Legendary chainmail, light and strong.", gold_value=50)

class WoodenShield(Armor):
    def __init__(self):
        super().__init__("Wooden Shield", 1, "A basic wooden shield.", gold_value=7)

class FireBomb(Item):
    def __init__(self):
        super().__init__("Fire Bomb", "Deals fire damage to all enemies.", item_type="consumable", gold_value=20)

class ScrollOfFireball(Item):
    def __init__(self):
        super().__init__("Scroll of Fireball", "Casts a powerful fireball.", item_type="scroll", gold_value=30)

class AmuletOfLuck(Item):
    def __init__(self):
        super().__init__("Amulet of Luck", "Increases your luck in battle.", item_type="accessory", gold_value=25)

class SilverRing(Item):
    def __init__(self):
        super().__init__("Silver Ring", "A simple silver ring.", item_type="accessory", gold_value=8)

class SingingSword(Weapon):
    def __init__(self):
        super().__init__("Singing Sword", 5, "A sword that sings when swung.", gold_value=40)