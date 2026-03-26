import json
import os
from characters.player import Player
from characters.race import Human    # We recreate the equipment
from items_and_equipment.equipment import Equipment
from items_and_equipment import items as item_classes

# A dictionary that maps item names (strings) to their actual classes.
# This is crucial for recreating item objects from the save file.
# IMPORTANT: Item classes MUST have a parameterless __init__() method to work with auto-discovery.
# If an item fails to instantiate, it will be logged and skipped during save/load.

# Build AVAILABLE_ITEMS by instantiating each subclass and using instance.name
AVAILABLE_ITEMS = {}
failed_items = []
for base in [item_classes.Item, item_classes.Weapon, item_classes.Armor]:
    for cls in base.__subclasses__():
        try:
            instance = cls()
            AVAILABLE_ITEMS[instance.name] = cls
        except Exception as e:
            # Log failed items to help developers debug issues
            failed_items.append(f"  - {cls.__name__}: {str(e)}")

if failed_items:
    print("[SAVE/LOAD WARNING] Failed to auto-discover the following item classes:")
    print("\n".join(failed_items))
    print("Ensure these classes have parameterless __init__() methods.")
else:
    print(f"✓ Successfully discovered {len(AVAILABLE_ITEMS)} item classes for save/load.")

SAVE_DIR = "saves" # Folder where save files will be stored

# Make sure the save folder exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_player_to_json(player):
    """
    Saves the player object's state to a JSON file.
    :param player: The Player object to save.
    """
    player_data = {
        "name": player.name,
        "level": player.level,
        "attack_power": player._attack_power,
        "hit_points_max": player._hit_points_max,
        "hit_points": player._hit_points,
        "experience": player.experience,
        "gold": player.gold,
        "unspent_attribute_points": player.unspent_attribute_points,
        "attribute_strength": player.attribute_strength,
        "attribute_dexterity": player.attribute_dexterity,
        "attribute_intelligence": player.attribute_intelligence,
        "race": player.race.name,
        "race_skills": player.race.get_skills_dict() if hasattr(player.race, 'get_skills_dict') else [],
        "equipment": {
            "weapon": player.equipment.weapon.name if player.equipment.weapon else None,
            "armor": player.equipment.armor.name if player.equipment.armor else None,
            "helmet": player.equipment.helmet.name if player.equipment.helmet else None,
            "shield": player.equipment.shield.name if player.equipment.shield else None,
            "accessory": player.equipment.accessory.name if hasattr(player.equipment, 'accessory') and player.equipment.accessory else None
        },
        "inventory": [item.name for item in player.inventory] # Save names of items in inventory
    }
    
    filename = os.path.join(SAVE_DIR, f"player_{player.name}.json")
    with open(filename, 'w') as f:
        json.dump(player_data, f, indent=4)
    print(f"Player '{player.name}' saved to {filename}")

def load_player_from_json(filename):
    """
    Loads a player object's state from a JSON file.
    :param filename: The name of the save file (e.g., "player_HeroName.json").
    :return: Loaded Player object or None if loading fails.
    """
    filepath = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Error: Save file not found at {filepath}")
        return None

    with open(filepath, 'r') as f:
        player_data = json.load(f)
    
    # We recreate the Player object
    player = Player(player_data["name"])
    player.level = player_data["level"]
    player.experience = player_data["experience"]
    player.gold = player_data["gold"]
    player.unspent_attribute_points = player_data["unspent_attribute_points"]
    player.attribute_strength = player_data["attribute_strength"]
    player.attribute_dexterity = player_data["attribute_dexterity"]
    player.attribute_intelligence = player_data["attribute_intelligence"]
    
    # We recreate the base stats (HP and Attack Power)
    player._hit_points_max = player_data["hit_points_max"]
    player.hit_points = player_data["hit_points"] # The setter will handle the alive status
    player.attack_power = player_data["attack_power"] # The setter will handle the value


    # Restore race and skills
    race_name = player_data["race"]
    if race_name == "Human":
        player.race = Human()
    elif race_name == "Elf":
        from characters.race import Elf
        player.race = Elf()
    elif race_name == "Dwarf":
        from characters.race import Dwarf
        player.race = Dwarf()
    elif race_name == "Orc":
        from characters.race import Orc
        player.race = Orc()
    # Skills are tied to race, so restoring race restores skills.

    # We recreate the equipment using AVAILABLE_ITEMS
    eq = player_data["equipment"]
    missing_equipment = []
    for slot in ["weapon", "armor", "helmet", "shield", "accessory"]:
        if eq.get(slot):
            item_name = eq[slot]
            if item_name in AVAILABLE_ITEMS:
                player.equipment.equip(AVAILABLE_ITEMS[item_name]())
            else:
                missing_equipment.append(f"  - {slot}: {item_name} (not found in AVAILABLE_ITEMS)")
    
    if missing_equipment:
        print(f"[SAVE/LOAD WARNING] Failed to restore some equipment for '{player.name}':")
        print("\n".join(missing_equipment))

    # Restore inventory
    if "inventory" in player_data:
        missing_inventory = []
        for item_name in player_data["inventory"]:
            if item_name in AVAILABLE_ITEMS:
                player.inventory.append(AVAILABLE_ITEMS[item_name]())
            else:
                missing_inventory.append(f"  - {item_name}")
        
        if missing_inventory:
            print(f"[SAVE/LOAD WARNING] Failed to restore some inventory items for '{player.name}':")
            print("\n".join(missing_inventory))

    print(f"Player '{player.name}' loaded successfully.")
    return player

def get_all_save_files():
    """
    Returns a list of all player save filenames in the SAVE_DIR.
    """
    if not os.path.exists(SAVE_DIR):
        return []
    
    save_files = [f for f in os.listdir(SAVE_DIR) if f.startswith("player_") and f.endswith(".json")]
    return save_files