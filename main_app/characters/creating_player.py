# --- IMPORT CHANGE ---
from .race import Human, Elf, Dwarf, Orc
from items_and_equipment.items import NarrowSword, BigStick, LeatherArmor, BasicPotion

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
    }
}