# Copilot Instructions for Munchkin-style RPG

## Project Overview
A Pygame-based turn-based RPG inspired by the card game "Munchkin". Features character creation with races, combat with monsters, equipment management, experience/leveling, and save/load functionality. **Recently updated with fullscreen mode and programmatic Munchkin-style graphics system.**

## Architecture & Data Flow

### Core State Machine: Game.py
[game.py](../main_app/game.py) manages the entire application lifecycle:
- Initializes Pygame in **fullscreen mode** (pygame.FULLSCREEN), AssetManager, and all screen objects
- Maintains game state as strings: `'main_menu'`, `'character_creation'`, `'load_game'`, `'game_world'`, `'fight'`, `'post_fight_summary'`, `'inventory'`
- Stores the active Player instance and passes it between screens via `self.player`
- **Key workflow**: State changes trigger screen swaps via `change_state()` method; player data persists across screens
- **New**: Added inventory screen state for equipment/item management

### Screen Architecture (MVC-like)
All screen classes (MainMenuScreen, CharacterCreationScreen, etc.) follow this pattern:
- Constructor receives `game` and `asset_manager` to access game state and resources
- `handle_events(events)` processes user input and game logic
- `draw(screen)` renders UI and calls `asset_manager.get_image()` or `asset_manager.get_font()`
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
Each race (Human, Elf, Dwarf, Orc, Halfling, Gnome, Half-Elf, Half-Orc) is a class with:
- `apply_bonuses()` - modifies player stats (attack_power, hit_points, etc.)
- `skills` dict - maps skill names (strings) to lambda functions returning bool for dodge/block mechanics

### Items & Equipment Flow
Items are instantiated from classes ([items.py](../main_app/items_and_equipment/items.py)); Equipment manages five slots (weapon, armor, helmet, shield, accessory). **Critical for save/load**: Item instances are recreated from JSON using `AVAILABLE_ITEMS` lookup by name in [save_and_load_player.py](../main_app/saving_data/save_and_load_player.py).

## Essential Patterns & Conventions

### Asset Loading & Graphics System
**CRITICAL UPDATE**: All graphics are now **programmatically generated** instead of loaded from files:
- **AssetManager** (asset_manager.py) creates Munchkin-style graphics on startup:
  - `_create_munchkin_graphics()` - Main graphics generation method
  - Backgrounds: `_create_main_menu_bg()`, `_create_character_creation_bg()`, etc.
  - UI Panels: `_create_player_card()`, `_create_monster_card()`
  - Buttons: `_create_button_normal()`, `_create_button_hover()`, `_create_button_selected()`
  - Item Icons: `_create_item_icons()` - Programmatic icons for all item types
- **Fonts**: `asset_manager.get_font('small'|'medium'|'large'|'title')`
- **Images**: `asset_manager.get_image('main_menu'|'player_card'|'weapon_icon'|...)`
- **Colors**: Bright Munchkin palette (red, blue, yellow, black outlines, parchment backgrounds)
- **No external assets required** - All graphics generated algorithmically

### Save/Load Serialization
- `save_player_to_json(player)` → writes to `saves/player_{name}.json`
- `load_player_from_json(filename)` → reconstructs Player with inventory and equipment by name lookup
- **Important**: Item classes must be instantiable with no args; equipment bonuses are NOT stored in JSON

### Combat & Monster Generation
- Monsters instantiated from `MONSTER_LIST` dict in [monster_list.py](../main_app/characters/monster_list.py)
- FightScreen triggers `player.attack()` → `monster.take_damage()` → check monster alive → award XP/loot on victory
- Loot drops as Item instances added to inventory; use `random.choice()` from MONSTER_LIST for encounters

### UI & Input Handling
- **Button class** (button.py) wraps action callbacks; hover/click logic in `handle_event()` and `draw()`
- **Updated**: Buttons now receive `asset_manager` parameter and use programmatic graphics
- **InputBox** (input_box.py) captures text; use for character naming in creation screen
- **Inventory Screen** (inventory_screen.py): New screen for equipment/item management with drag-and-drop
- All UI positions are absolute pixel coordinates; reference SCREEN_WIDTH/HEIGHT (1280×800) constants
- **Fullscreen mode**: Game runs in pygame.FULLSCREEN for immersive experience

## Common Development Tasks

### Adding a New Item
1. Create subclass in [items.py](../main_app/items_and_equipment/items.py) inheriting from Item, Weapon, or Armor
2. Item class must have parameterless `__init__` (used by AVAILABLE_ITEMS auto-discovery)
3. Set `name` property in super().__init__(); this string key is used in save/load
4. **New**: Item icons are automatically generated in `asset_manager._create_item_icons()`

### Adding a New Monster
1. Create instance in [monster_list.py](../main_app/characters/monster_list.py) inheriting from Monster
2. Add to MONSTER_LIST dict with string key
3. Monsters use BaseCharacter stats (level, attack_power, hit_points); customize loot drops

### Adding a New Screen
1. Create class in main_app/ following the pattern (MainMenuScreen, etc.)
2. Implement `handle_events(events)` and `draw(screen)` methods
3. Register in Game._initialize_screens() with state string key
4. Call `game.change_state()` to switch from buttons
5. **Updated**: Pass `asset_manager` to constructor for graphics access

### Adding Programmatic Graphics
1. Add creation method to AssetManager (e.g., `_create_new_panel()`)
2. Call it from `_create_munchkin_graphics()`
3. Store result in `self.images['key_name']`
4. Use `asset_manager.get_image('key_name')` in screen classes
5. Follow Munchkin color scheme: bright primaries, black outlines, parchment backgrounds

### Modifying Game State Persistence
- Edit `save_player_to_json()` to add new fields to player_data dict
- Edit `load_player_from_json()` to reconstruct those fields
- **Always** test save→quit→load cycle for regression

## Configuration & Paths
- **Screen dimensions**: 1280×800 (constants.py) - hardcoded for UI layout
- **Display mode**: pygame.FULLSCREEN for immersive gameplay
- **Font**: MedievalSharp-Regular.ttf loaded via AssetManager
- **Save directory**: `main_app/saves/` (relative to working directory)
- **Graphics**: All assets generated programmatically - no external files required
- **Colors**: Munchkin palette (red, blue, yellow, black outlines, parchment #FFFFF8DC)

## Common Gotchas
- **Don't re-instantiate Game**: Use `game.player` to access current player across screens
- **Race bonuses aren't auto-applied**: Call `player.apply_race_bonuses()` after race selection
- **Item recreation in save/load fails silently**: If AVAILABLE_ITEMS doesn't find item class, inventory is corrupted
- **Equipment stats not saved**: Item bonuses recalculate on equip via `apply_item_bonus()` (currently placeholder)
- **NEW: Graphics are programmatic**: Don't try to load image files - use `asset_manager.get_image()`
- **NEW: Screen method names**: Use `handle_events(events)` not `update(events)`
- **NEW: Button constructor**: Always pass `asset_manager` parameter to Button()
- **NEW: Fullscreen mode**: UI is hardcoded for 1280×800 - changing resolution breaks layout
