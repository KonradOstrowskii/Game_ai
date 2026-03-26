# Munchkin-style RPG

## Introduction

A classic-style RPG where you fight monsters, gain experience, and collect loot. This game is inspired by the card game "Munchkin" and focuses on a fun and engaging gameplay loop. Create your character, choose your race, and venture into a world of adventure!

## Features

*   **Character Creation:** Create your own character and choose from four different races: Human, Elf, Dwarf, and Orc.
*   **Race-Specific Skills:** Each race has its own unique skills that can be used in combat (Dodge, Block, etc.).
*   **Turn-Based Combat:** Engage in turn-based combat with a variety of monsters.
*   **Experience and Leveling:** Gain experience from defeating monsters and level up your character to become more powerful.
*   **Equipment and Inventory:** Find and equip a wide variety of items, including weapons, armor, and potions. Manage your inventory and choose the best gear for your character.
*   **Random Loot Drops:** Defeated monsters have a chance to drop valuable loot. The quality and type of loot depend on the monster's difficulty.
*   **Save and Load:** Save your game progress at any time and continue your adventure later.

## Project Structure

```
main_app/
├── game.py                    # Core game state machine & main loop
├── main_app.py               # Entry point
├── constants.py              # Screen size, colors, paths
├── asset_manager.py          # Font/image caching
├── characters/
│   ├── player.py             # Player character with XP/leveling
│   ├── base_character.py     # Base combat mechanics (HP, attack)
│   ├── monster.py            # Monster template
│   ├── monster_list.py       # All monster definitions & loot tables
│   └── race.py               # Race classes (Human, Elf, Dwarf, Orc)
├── items_and_equipment/
│   ├── items.py              # Item definitions (weapons, armor, potions)
│   └── equipment.py          # Equipment slots & equip logic
├── saves/                    # Auto-created save files (JSON)
└── saving_data/
    └── save_and_load_player.py  # Serialization logic
```

## For Developers

- **Architecture Guide**: See [.github/copilot-instructions.md](./.github/copilot-instructions.md) for deep dives into state machine, combat system, and design patterns
- **Setup**: See [GETTING_STARTED.md](./GETTING_STARTED.md) for dev environment setup
- **Robustness Improvements**: See [PAIN_POINTS_FIXES.md](./PAIN_POINTS_FIXES.md) for asset validation, logging, and input validation improvements
- **Combat Improvements**: See [COMBAT_UI_IMPROVEMENTS.md](./COMBAT_UI_IMPROVEMENTS.md) for fight log display and refactored combat logic
- **Key Files**: 
  - `game.py` - State management + asset validation
  - `characters/base_character.py` - Combat mechanics with cleaner skill logic
  - `saving_data/save_and_load_player.py` - Persistence with detailed logging

### TL;DR
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install pygame
cd main_app
python main_app.py
```

### Prerequisites

*   Python 3.8+
*   Pygame (installed via pip)

### How to Play

1. **Create Character**: Choose name and race (Human/Elf/Dwarf/Orc)
2. **Fight Monsters**: Click "Fight" to encounter random enemies
3. **Collect Loot**: Equip items from defeated monsters
4. **Level Up**: Gain XP to improve stats
5. **Save Progress**: Game auto-saves; load saved characters on startup

## Future Development

*   Adding more character classes with unique abilities.
*   Implementing a quest system.
*   Creating a world map to explore.
*   Adding more monsters, items, and skills.
*   Developing a crafting system.


**Issues during gameplay?** Check console output for error messages (game runs in terminal).


