# main_app/fight_screen.py

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from button import Button
from characters.monster_list import MONSTER_LIST

class FightScreen:
    """
    Screen for handling combat encounters between the player and a monster.
    """
    def __init__(self, game, asset_manager):
        self.game = game
        self.asset_manager = asset_manager
        self.player = None
        self.monster = None
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((100, 100, 100))

        self.attack_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 150, 200, 60, "Attack",
                                   action=self.player_attack)
        self.use_item_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 220, 200, 60, "Use Item",
                                     action=self.use_item)
        self.run_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 70, 200, 60, "Run Away",
                                action=self.run_away)
        self.back_to_world_button = Button(50, 50, 200, 60, "Back to World",
                                          action=lambda: self.game.change_state('game_world'))
        self.fight_log = []
        self.log_scroll = 0  # For scrolling through fight log

    def start_new_fight(self, player):
        """Sets up a new fight with the given player."""
        self.player = player
        monster_key = random.choice(list(MONSTER_LIST.keys()))
        self.monster = MONSTER_LIST[monster_key]
        self.fight_log = [f"A {self.monster.name} appears!"]

    def player_attack(self):
        """Handles player's attack action."""
        if self.player and self.monster:
            # Check for dodge/block before attack
            initial_hp = self.monster.hit_points
            
            self.player.attack(self.monster)
            
            # Determine what happened based on HP change
            hp_change = initial_hp - self.monster.hit_points
            if hp_change == 0:
                # Must have been dodged
                self.fight_log.append(f"{self.monster.name} dodged {self.player.name}'s attack!")
            else:
                self.fight_log.append(f"{self.player.name} attacks {self.monster.name}, dealing {hp_change} damage.")
            
            if not self.monster.alive:
                self.fight_log.append(f"{self.monster.name} is defeated!")
                from characters.monster_list import roll_loot
                looted_items = roll_loot(self.monster)
                
                # Check inventory space before adding loot
                added_items = []
                rejected_items = []
                for item in looted_items:
                    if len(self.player.inventory) < self.player.max_inventory_slots:
                        self.player.inventory.append(item)
                        added_items.append(item.name)
                    else:
                        rejected_items.append(item.name)
                
                self.game.last_fight_rewards = {
                    "monster_name": self.monster.name,
                    "xp": self.monster.experience_reward,
                    "gold": self.monster.treasure_reward,
                    "items": added_items,
                    "rejected_items": rejected_items
                }
                self.fight_log.append(f"You gained {self.monster.experience_reward} XP!")
                if added_items:
                    self.fight_log.append(f"Looted: {', '.join(added_items)}")
                if rejected_items:
                    self.fight_log.append(f"Inventory full! Couldn't carry: {', '.join(rejected_items)}")
                self.player.gain_experience(self.monster.experience_reward)
                self.player.gold += self.monster.treasure_reward
                self.game.save_player_to_json(self.player)
                self.game.change_state('post_fight_summary')
            else:
                self.monster_attack()
        else:
            self.game.message = "Error: No player or monster in fight."

    def use_item(self):
        """Handles player's item usage action."""
        if self.player:
            # Check quick slots first for potions
            for i, item in enumerate(self.player.equipment.quick_slots):
                if item and item.item_type == "potion":
                    self.use_potion(item, quick_slot_index=i)
                    return
            
            # If no potions in quick slots, check regular inventory
            for item in self.player.inventory:
                if item.item_type == "potion":
                    self.use_potion(item)
                    return
            
            self.fight_log.append("No potions available!")
        else:
            self.fight_log.append("No items to use!")

    def use_potion(self, potion, quick_slot_index=None):
        """Uses a potion and applies its effects."""
        if potion.name == "Healing Potion":
            heal_amount = min(20, self.player._hit_points_max - self.player.hit_points)
            self.player.hit_points += heal_amount
            self.fight_log.append(f"Used {potion.name}, healed {heal_amount} HP!")
        elif potion.name == "Greater Healing Potion":
            heal_amount = min(50, self.player._hit_points_max - self.player.hit_points)
            self.player.hit_points += heal_amount
            self.fight_log.append(f"Used {potion.name}, healed {heal_amount} HP!")
        elif potion.name == "Mana Potion":
            # For now, just log it (no mana system yet)
            self.fight_log.append(f"Used {potion.name}, restored 20 MP!")
        elif potion.name == "Greater Mana Potion":
            self.fight_log.append(f"Used {potion.name}, restored 50 MP!")
        elif potion.name == "Strength Potion":
            self.player.attack_power += 3
            self.fight_log.append(f"Used {potion.name}, attack increased by 3!")
        elif potion.name == "Defense Potion":
            # Could add temporary defense bonus
            self.fight_log.append(f"Used {potion.name}, defense increased by 3!")
        elif potion.name == "Speed Potion":
            self.fight_log.append(f"Used {potion.name}, dodge chance increased!")
        elif potion.name == "Regeneration Potion":
            self.fight_log.append(f"Used {potion.name}, regeneration active for 3 turns!")
        elif potion.name == "Antidote Potion":
            self.fight_log.append(f"Used {potion.name}, poison cured!")
        elif potion.name == "Elixir of Life":
            self.player.hit_points = self.player._hit_points_max
            self.fight_log.append(f"Used {potion.name}, fully healed!")
        
        # Remove the used potion
        if quick_slot_index is not None:
            self.player.equipment.quick_slots[quick_slot_index] = None
        else:
            self.player.inventory.remove(potion)
        
        # Monster gets a turn after using item
        if self.monster and self.monster.alive:
            self.monster_attack()

    def monster_attack(self):
        """Handles monster's attack action."""
        if self.player and self.monster and self.monster.alive:
            initial_hp = self.player.hit_points
            
            self.monster.attack(self.player)
            
            # Determine what happened based on HP change
            hp_change = initial_hp - self.player.hit_points
            if hp_change == 0:
                # Must have been dodged
                self.fight_log.append(f"{self.player.name} dodged {self.monster.name}'s attack!")
            else:
                self.fight_log.append(f"{self.monster.name} attacks {self.player.name}, dealing {hp_change} damage.")
            
            if not self.player.alive:
                self.fight_log.append(f"{self.player.name} is defeated! Game Over!")
                self.game.message = "Game Over!"
                self.game.change_state('main_menu')
        
    def run_away(self):
        """Handles player's attempt to run away from the fight."""
        self.fight_log.append(f"{self.player.name} attempts to run away!")
        self.game.message = f"{self.player.name} successfully ran away!"
        self.game.change_state('game_world')

    def handle_events(self, events):
        """Handles user input events for this screen."""
        for event in events:
            self.attack_button.handle_event(event)
            self.use_item_button.handle_event(event)
            self.run_button.handle_event(event)
            self.back_to_world_button.handle_event(event)

    def draw(self, screen):
        """Draws the fight screen elements."""
        screen.blit(self.background, (0, 0))
        self.game.draw_text("Combat!", 'title', WHITE, SCREEN_WIDTH / 2, 50)

        if self.player and self.monster:
            # Draw player and monster stats at top
            self.game.draw_text(f"Player: {self.player.name} HP: {self.player.hit_points}/{self.player._hit_points_max}", 
                                'large', WHITE, SCREEN_WIDTH / 4, 150)
            self.game.draw_text(f"Monster: {self.monster.name} HP: {self.monster.hit_points}/{self.monster._hit_points_max}", 
                                'large', WHITE, SCREEN_WIDTH * 3 / 4, 150)

            # Draw larger fight log area
            log_width = 800
            log_height = 280
            log_x = SCREEN_WIDTH / 2 - log_width / 2
            log_y = 220
            
            # Background for log
            log_surface = pygame.Surface((log_width, log_height), pygame.SRCALPHA)
            log_surface.fill((40, 40, 40, 220))
            screen.blit(log_surface, (log_x, log_y))
            
            # Draw border around log
            pygame.draw.rect(screen, WHITE, (log_x, log_y, log_width, log_height), 2)
            
            # Draw log entries (show up to 10 lines)
            small_font = self.asset_manager.get_font('small')
            log_y_start = log_y + 10
            max_lines = 10
            start_index = max(0, len(self.fight_log) - max_lines)
            
            for i, entry in enumerate(self.fight_log[start_index:]):
                text_surface = small_font.render(entry, True, WHITE)
                screen.blit(text_surface, (log_x + 10, log_y_start + i * 28))
            
            # Draw scroll indicator if there are more messages
            if len(self.fight_log) > max_lines:
                scroll_text = f"↑ {len(self.fight_log) - max_lines} more messages ↑"
                self.game.draw_text(scroll_text, 'small', (200, 200, 200), SCREEN_WIDTH / 2, log_y + log_height + 10)

            # Draw buttons at bottom
            font_medium = self.asset_manager.get_font('medium')
            if self.player.alive and self.monster.alive:
                self.attack_button.draw(screen, font_medium)
                self.use_item_button.draw(screen, font_medium)
                self.run_button.draw(screen, font_medium)
            else:
                self.back_to_world_button.draw(screen, font_medium)
        else:
            self.game.draw_text("No active fight.", 'large', WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)