from characters.monster import Monster
from items_and_equipment import items
import random

# Each loot_table is a list of tuples: (item class, drop_chance in %, min_qty, max_qty)
MONSTER_LIST = {
    "goblin": Monster("Goblin", 1, 5, 10, experience_reward=10, treasure_reward=1),
    "orc_warrior": Monster("Orc Warrior", 2, 8, 20, experience_reward=25, treasure_reward=2),
    "troll": Monster("Troll", 3, 12, 35, experience_reward=50, treasure_reward=3),
    "giant_spider": Monster("Giant Spider", 2, 7, 15, experience_reward=20, treasure_reward=1),
    "skeleton": Monster("Skeleton", 1, 6, 12, experience_reward=12, treasure_reward=1),
    # High-level monsters:
    "dragon": Monster("Dragon", 10, 25, 120, experience_reward=200, treasure_reward=20),
    "lich": Monster("Lich", 8, 18, 80, experience_reward=120, treasure_reward=12),
    "ogre_chief": Monster("Ogre Chief", 6, 20, 60, experience_reward=90, treasure_reward=8),
}

# Attach loot tables to each monster (by .loot_table attribute)
MONSTER_LIST["goblin"].loot_table = [
    (items.RustySword, 10, 1, 1),
    (items.BasicPotion, 20, 1, 1),
    (items.SilverRing, 5, 1, 1),
]
MONSTER_LIST["orc_warrior"].loot_table = [
    (items.BigStick, 15, 1, 1),
    (items.LeatherArmor, 10, 1, 1),
    (items.HealthPotion, 20, 1, 1),
    (items.AmuletOfLuck, 5, 1, 1),
]
MONSTER_LIST["troll"].loot_table = [
    (items.MithrilChainmail, 3, 1, 1),
    (items.HealthPotion, 30, 1, 2),
    (items.FireBomb, 10, 1, 1),
    (items.SingingSword, 2, 1, 1),
]
MONSTER_LIST["giant_spider"].loot_table = [
    (items.BasicPotion, 25, 1, 1),
    (items.ManaPotion, 10, 1, 1),
    (items.ScrollOfFireball, 5, 1, 1),
]
MONSTER_LIST["skeleton"].loot_table = [
    (items.IronHelmet, 8, 1, 1),
    (items.WoodenShield, 12, 1, 1),
    (items.BasicPotion, 20, 1, 1),
]
MONSTER_LIST["dragon"].loot_table = [
    (items.MithrilChainmail, 20, 1, 1),
    (items.SingingSword, 10, 1, 1),
    (items.AmuletOfLuck, 25, 1, 1),
    (items.HealthPotion, 50, 1, 2),
    (items.ScrollOfFireball, 30, 1, 1),
]
MONSTER_LIST["lich"].loot_table = [
    (items.ScrollOfFireball, 40, 1, 2),
    (items.ManaPotion, 60, 1, 2),
    (items.AmuletOfLuck, 15, 1, 1),
    (items.SilverRing, 30, 1, 1),
]
MONSTER_LIST["ogre_chief"].loot_table = [
    (items.BigStick, 30, 1, 1),
    (items.IronHelmet, 25, 1, 1),
    (items.WoodenShield, 40, 1, 1),
    (items.HealthPotion, 50, 1, 2),
]

# Helper for loot rolling
def roll_loot(monster):
    loot = []
    if hasattr(monster, "loot_table"):
        for item_class, chance, min_qty, max_qty in monster.loot_table:
            if random.randint(1, 100) <= chance:
                qty = random.randint(min_qty, max_qty)
                for _ in range(qty):
                    loot.append(item_class())
    return loot
