# --- IMPORT CHANGE ---
from .race import Human, Elf, Dwarf, Orc, Halfling, Gnome, HalfElf, HalfOrc
from items_and_equipment.items import NarrowSword, BigStick, LeatherArmor, BasicPotion, HealthPotion, ManaPotion

# Initial configuration for each race
RACE_CONFIG = {
    "human": {
        "class": Human,
        "items": [
            LeatherArmor(),
            BasicPotion()
        ]
    },
    "elf": {
        "class": Elf,
        "items": [
            NarrowSword(), # Elf starts with a Narrow Sword
            LeatherArmor(),
            BasicPotion()
        ]
    },
    "dwarf": {
        "class": Dwarf,
        "items": [
            LeatherArmor(), # Dwarves can start with basic armor
            BasicPotion()
        ]
    },
    "orc": {
        "class": Orc,
        "items": [
            BigStick(), # Orc starts with a Big Stick
            LeatherArmor(),
            BasicPotion()
        ]
    },
    "halfling": {
        "class": Halfling,
        "items": [
            LeatherArmor(),
            BasicPotion(),
            HealthPotion() # Halflings get an extra potion for luck
        ]
    },
    "gnome": {
        "class": Gnome,
        "items": [
            NarrowSword(),
            LeatherArmor(),
            ManaPotion() # Gnomes get mana potion for magic
        ]
    },
    "half-elf": {
        "class": HalfElf,
        "items": [
            NarrowSword(),
            LeatherArmor(),
            BasicPotion(),
            HealthPotion()
        ]
    },
    "half-orc": {
        "class": HalfOrc,
        "items": [
            BigStick(),
            LeatherArmor(),
            BasicPotion()
        ]
    }
}