# --- IMPORT CHANGE ---
from items_and_equipment.items import Item, Weapon, Armor

class Equipment:
    """
    Manages a character's equipped items (weapon, armor).
    """
    def __init__(self):
        self.weapon = None
        self.armor = None  # body armor
        self.helmet = None
        self.shield = None
        self.accessory = None
        self.other_items = [] # For potions, scrolls, etc.

    def equip(self, item):
        """
        Equips an item in the correct slot based on its type or name.
        :param item: The Item object to equip.
        :return: The previously equipped item (if any), or None if nothing was replaced.
        """
        if not isinstance(item, Item):
            print(f"Cannot equip {item}: Not an Item instance.")
            return None

        previous = None
        # Weapon
        if item.item_type == "weapon":
            if self.weapon:
                print(f"Unequipping {self.weapon.name} to equip {item.name}.")
                previous = self.weapon
            self.weapon = item
            print(f"Equipped {item.name} as weapon.")
            return previous
        # Armor (body)
        elif item.item_type == "armor":
            # Try to detect helmet or shield by name
            lname = item.name.lower()
            if "helmet" in lname or "cap" in lname or "hat" in lname:
                if self.helmet:
                    print(f"Unequipping {self.helmet.name} to equip {item.name}.")
                    previous = self.helmet
                self.helmet = item
                print(f"Equipped {item.name} as helmet.")
                return previous
            elif "shield" in lname:
                if self.shield:
                    print(f"Unequipping {self.shield.name} to equip {item.name}.")
                    previous = self.shield
                self.shield = item
                print(f"Equipped {item.name} as shield.")
                return previous
            else:
                if self.armor:
                    print(f"Unequipping {self.armor.name} to equip {item.name}.")
                    previous = self.armor
                self.armor = item
                print(f"Equipped {item.name} as body armor.")
                return previous
        # Accessory
        elif item.item_type == "accessory":
            if self.accessory:
                print(f"Unequipping {self.accessory.name} to equip {item.name}.")
                previous = self.accessory
            self.accessory = item
            print(f"Equipped {item.name} as accessory.")
            return previous
        else:
            # For items like potions, scrolls, etc.
            self.other_items.append(item)
            print(f"Added {item.name} to inventory.")
            return None

    def unequip(self, item_type):
        """
        Unequips an item of a given type/slot.
        :param item_type: "weapon", "armor", "helmet", "shield", "accessory".
        :return: The unequipped Item object, or None if nothing was unequipped.
        """
        if item_type == "weapon" and self.weapon:
            unequipped = self.weapon
            self.weapon = None
            print(f"Unequipped {unequipped.name}.")
            return unequipped
        elif item_type == "armor" and self.armor:
            unequipped = self.armor
            self.armor = None
            print(f"Unequipped {unequipped.name}.")
            return unequipped
        elif item_type == "helmet" and self.helmet:
            unequipped = self.helmet
            self.helmet = None
            print(f"Unequipped {unequipped.name}.")
            return unequipped
        elif item_type == "shield" and self.shield:
            unequipped = self.shield
            self.shield = None
            print(f"Unequipped {unequipped.name}.")
            return unequipped
        elif item_type == "accessory" and self.accessory:
            unequipped = self.accessory
            self.accessory = None
            print(f"Unequipped {unequipped.name}.")
            return unequipped
        else:
            print(f"No {item_type} equipped to unequip.")
            return None

    def __str__(self):
        weapon_str = self.weapon.name if self.weapon else "None"
        armor_str = self.armor.name if self.armor else "None"
        helmet_str = self.helmet.name if self.helmet else "None"
        shield_str = self.shield.name if self.shield else "None"
        accessory_str = self.accessory.name if self.accessory else "None"
        return (
            f"Weapon: {weapon_str}, Armor: {armor_str}, Helmet: {helmet_str}, "
            f"Shield: {shield_str}, Accessory: {accessory_str}"
        )