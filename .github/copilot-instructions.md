# Copilot Instructions for Munchkin-style RPG

## Project Overview
A Pygame-based turn-based RPG inspired by the card game "Munchkin". Features character creation with races, combat with monsters, equipment management, experience/leveling, and save/load functionality.

## Architecture & Data Flow

### Core State Machine: Game.py
[game.py](../main_app/game.py) manages the entire application lifecycle:
- Initializes Pygame, AssetManager, and all screen objects
- Maintains game state as strings: `'main_menu'`, `'character_creation'`, `'load_game'`, `'game_world'`, `'fight'`, `'post_fight_summary'`
- Stores the active Player instance and passes it between screens via `self.player`
- **Key workflow**: State changes trigger screen swaps via `change_state()` method; player data persists across screens

### Screen Architecture (MVC-like)
All screen classes (MainMenuScreen, CharacterCreationScreen, etc.) follow this pattern:
- Constructor receives `game` and `asset_manager` to access game state and resources
- `update()` processes events and game logic
- `draw()` renders UI and calls `asset_manager.get_image()` or `asset_manager.get_font()`
- Screens communicate back to Game via `game.change_state()` and modifying `game.player`

### Character System Hierarchy
```
BaseCharacter (base_character.py)
├── Player (player.py) - Adds inventory, equipment, race, XP/leveling
├── Monster (monster.py) - Generated from MONSTER_LIST
```
**Key mechanics**:
- HP and damage use property setters to clamp values and track `alive` status
- Combat: `BaseCharacter.attack()` calculates damage; target calls `take_damage()`
- Defensive skills (Dodge, Block) execute via `race.skills` dict during `take_damage()`
- **Level-up formula**: XP needed = `level * 100`; leveling grants +5 max HP, +2 attack, +1 attribute point

### Race & Skills System (characters/race.py)
Each race (Human, Elf, Dwarf, Orc) is a class with:
- `apply_bonuses()` - modifies player stats (attack_power, hit_points, etc.)
- `skills` dict - maps skill names (strings) to lambda functions returning bool for dodge/block mechanics

### Items & Equipment Flow
Items are instantiated from classes ([items.py](../main_app/items_and_equipment/items.py)); Equipment manages five slots (weapon, armor, helmet, shield, accessory). **Critical for save/load**: Item instances are recreated from JSON using `AVAILABLE_ITEMS` lookup by name in [save_and_load_player.py](../main_app/saving_data/save_and_load_player.py).

## Essential Patterns & Conventions

### Asset Loading
**Always** use AssetManager (asset_manager.py):
- Fonts: `asset_manager.get_font('small'|'medium'|'large'|'title')`
- Images: `asset_manager.get_image('menu_background'|...)` (returns pygame.Surface or None)
- Path constants in [constants.py](../main_app/constants.py) define all asset locations

### Save/Load Serialization
- `save_player_to_json(player)` → writes to `saves/player_{name}.json`
- `load_player_from_json(filename)` → reconstructs Player with inventory and equipment by name lookup
- **Important**: Item classes must be instantiable with no args; equipment bonuses are NOT stored in JSON

### Combat & Monster Generation
- Monsters instantiated from `MONSTER_LIST` dict in [monster_list.py](../main_app/characters/monster_list.py)
- FightScreen triggers `player.attack()` → `monster.take_damage()` → check monster alive → award XP/loot on victory
- Loot drops as Item instances added to inventory; use `random.choice()` from MONSTER_LIST for encounters

### UI & Input Handling
- Button class wraps action callbacks; hover/click logic in `update()` and `draw()`
- InputBox (input_box.py) captures text; use for character naming in creation screen
- All UI positions are absolute pixel coordinates; reference SCREEN_WIDTH/HEIGHT (1280×800) constants

## Common Development Tasks

### Adding a New Item
1. Create subclass in [items.py](../main_app/items_and_equipment/items.py) inheriting from Item, Weapon, or Armor
2. Item class must have parameterless `__init__` (used by AVAILABLE_ITEMS auto-discovery)
3. Set `name` property in super().__init__(); this string key is used in save/load

### Adding a New Monster
1. Create instance in [monster_list.py](../main_app/characters/monster_list.py) inheriting from Monster
2. Add to MONSTER_LIST dict with string key
3. Monsters use BaseCharacter stats (level, attack_power, hit_points); customize loot drops

### Adding a New Screen
1. Create class in main_app/ inheriting from "screen template" (e.g., MainMenuScreen)
2. Implement `update(events)` and `draw(surface)` methods
3. Register in Game._initialize_screens() with state string key
4. Call `game.change_state()` to switch from buttons

### Modifying Game State Persistence
- Edit `save_player_to_json()` to add new fields to player_data dict
- Edit `load_player_from_json()` to reconstruct those fields
- **Always** test save→quit→load cycle for regression

## Configuration & Paths
- Screen dimensions: 1280×800 (constants.py)
- Font: MedievalSharp-Regular.ttf (hardcoded in constants.py)
- Save directory: `main_app/saves/` (relative to working directory)
- If assets missing: AssetManager falls back to pygame defaults with warning to console

## Common Gotchas
- **Don't re-instantiate Game**: Use `game.player` to access current player across screens
- **Race bonuses aren't auto-applied**: Call `player.apply_race_bonuses()` after race selection
- **Item recreation in save/load fails silently**: If AVAILABLE_ITEMS doesn't find item class, inventory is corrupted
- **Equipment stats not saved**: Item bonuses recalculate on equip via `apply_item_bonus()` (currently placeholder)
