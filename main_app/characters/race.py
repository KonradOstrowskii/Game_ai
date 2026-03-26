import random

class Race:
    """Base class for all character races."""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.skills = {} # Now supports skills

    def apply_bonuses(self, player):
        """
        Applies race-specific attribute bonuses to the player.
        This method must be overridden by subclasses.
        :param player: The Player object.
        """
        pass

    def add_skill(self, skill_name, skill_function=None):
        """Adds a skill to the race's skill dictionary."""
        if skill_function is not None:
            self.skills[skill_name] = skill_function

    def get_skills_dict(self):
        """Returns a list of skill names for saving/display purposes."""
        return list(self.skills.keys())
        
    def __str__(self):
        return self.description

class Human(Race):
    def __init__(self):
        description = ("Humans are versatile and adaptable. While they don't excel in one area, "
                       "they possess a unique determination. This grants them a chance for an **Adrenaline Rush** "
                       "when their health is low, allowing them to strike back with surprising force.")
        super().__init__("Human", description)
        self.add_skill("Adrenaline Rush", self.adrenaline_rush)

    def apply_bonuses(self, player):
        player.attack_power += 1
        player._hit_points_max += 2
        player.hit_points += 2 # Restore current HP
        player.attribute_strength += 1
        player.attribute_dexterity += 1
        player.attribute_intelligence += 1

    @staticmethod
    def adrenaline_rush():
        """Checks if the Human's Adrenaline Rush triggers (20% chance)."""
        return random.randint(1, 5) == 5

# --- ELF: Agility and Evasion (Dodge) ---
class Elf(Race):
    def __init__(self):
        description = ("Elves are graceful and intelligent beings, known for their agility and keen senses. "
                       "As an Elf, you possess a unique **20% chance to Dodge** incoming attacks, "
                       "showcasing your exceptional reflexes and evasive skills. They gain a significant bonus to Dexterity.")
        super().__init__("Elf", description)
        self.add_skill("Dodge", self.dodges)

    def apply_bonuses(self, player):
        player.attack_power += 2 # Bonus to attack from Agility
        player._hit_points_max += 1 # Less HP than others
        player.hit_points += 1
        player.attribute_dexterity += 3 # Large bonus to Dexterity
        player.attribute_intelligence += 1

    @staticmethod
    def dodges():
        """Checks if the Elf successfully dodges an attack (20% chance, 1 in 5)."""
        return random.randint(1, 5) == 5

# --- DWARF: Resilience and Defense (Block) ---
class Dwarf(Race):
    def __init__(self):
        description = ("Dwarves are sturdy and resilient, known for their hardy constitution and love of gold. "
                       "Your natural toughness grants you a **20% chance to Block** (mitigate) incoming damage. "
                       "You receive a large bonus to maximum HP and Strength, but a slight penalty to Intelligence.")
        super().__init__("Dwarf", description)
        self.add_skill("Block", self.block)

    def apply_bonuses(self, player):
        player.attack_power += 1
        player._hit_points_max += 5 # Large HP bonus
        player.hit_points += 5
        player.attribute_strength += 2 # Strength bonus
        player.attribute_intelligence -= 1 # Small Intelligence penalty

    @staticmethod
    def block():
        """Checks if the Dwarf successfully blocks an attack (20% chance, 1 in 5)."""
        return random.randint(1, 5) == 5

# --- ORC: Strength and Battle Fury (Berserk) ---
class Orc(Race):
    def __init__(self):
        description = ("Orcs are brutal and powerful creatures, eager for battle and glory. "
                       "You have a **20% chance to activate Battle Fury (Berserk)**, allowing you to deal "
                       "significantly increased damage on your next attack. They gain large bonuses to Attack Power and Strength, "
                       "but suffer a penalty to Dexterity.")
        super().__init__("Orc", description)
        self.add_skill("Berserk", self.berserk)

    def apply_bonuses(self, player):
        player.attack_power += 3 # Large attack bonus
        player._hit_points_max += 3
        player.hit_points += 3
        player.attribute_strength += 3 # Large Strength bonus
        player.attribute_dexterity -= 1 # Small Dexterity penalty

    def berserk(self):
        """Check if the Orc's Battle Fury triggers (20% chance, 1 in 5)."""
        return random.randint(1, 5) == 5