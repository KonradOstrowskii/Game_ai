# main_app/fight_screen.py

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHT_GRAY, GOLD
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
                                   action=self.player_attack, asset_manager=asset_manager)
        self.use_item_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 220, 200, 60, "Use Item",
                                     action=self.use_item, asset_manager=asset_manager)
        self.run_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 70, 200, 60, "Run Away",
                                action=self.run_away, asset_manager=asset_manager)
        self.back_to_world_button = Button(50, 50, 200, 60, "Back to World",
                                          action=lambda: self.game.change_state('game_world'), asset_manager=asset_manager)
        self.fight_log = []
        self.log_scroll = 0  # For scrolling through fight log
        self.potion_buttons = []  # For clickable potions

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
            
            # Handle potion button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for potion_button in self.potion_buttons:
                    potion_button.handle_event(event)

    def draw(self, screen):
        """Draws the fight screen elements."""
        screen.blit(self.background, (0, 0))
        self.game.draw_text("Combat!", 'title', WHITE, SCREEN_WIDTH / 2, 50)
        
        # Clear potion buttons
        self.potion_buttons = []

        if self.player and self.monster:
            # Draw player and monster stats at top
            self.game.draw_text(f"Player: {self.player.name} HP: {self.player.hit_points}/{self.player._hit_points_max}", 
                                'large', WHITE, SCREEN_WIDTH / 4, 100)
            self.game.draw_text(f"Monster: {self.monster.name} HP: {self.monster.hit_points}/{self.monster._hit_points_max}", 
                                'large', WHITE, SCREEN_WIDTH * 3 / 4, 100)

            # Draw larger fight log area
            log_width = 800
            log_height = 200
            log_x = SCREEN_WIDTH / 2 - log_width / 2
            log_y = 150
            
            # Background for log
            log_surface = pygame.Surface((log_width, log_height), pygame.SRCALPHA)
            log_surface.fill((40, 40, 40, 220))
            screen.blit(log_surface, (log_x, log_y))
            
            # Draw border around log
            pygame.draw.rect(screen, WHITE, (log_x, log_y, log_width, log_height), 2)
            
            # Draw log entries (show up to 8 lines)
            small_font = self.asset_manager.get_font('small')
            log_y_start = log_y + 10
            max_lines = 8
            start_index = max(0, len(self.fight_log) - max_lines)
            
            for i, entry in enumerate(self.fight_log[start_index:]):
                text_surface = small_font.render(entry, True, WHITE)
                screen.blit(text_surface, (log_x + 10, log_y_start + i * 22))
            
            # Draw info panels below log with dynamic heights
            panel_y = log_y + log_height + 20
            padding = 12
            panel_width = 180
            
            # Get data for all panels
            player_skills_data = self._get_player_skills()
            player_stats_data = self._get_player_stats()
            potion_data = self._get_potion_and_equip_info()
            monster_skills_data = self._get_monster_skills()
            
            # Calculate panel height based on longest content set
            content_lines = max(len(player_skills_data), len(player_stats_data), len(potion_data) + len(self.player.equipment.quick_slots), len(monster_skills_data))
            panel_height = self._calculate_panel_height(small_font, content_lines)
            panel_height = min(max(panel_height, 180), 260)
            
            # Left side: player's stuff (skills, potions/equipment)
            left_x = 30
            self._draw_info_panel(screen, left_x, panel_y, panel_width, panel_height, 
                                 "PLAYER SKILLS", player_skills_data, small_font)
            self._draw_potion_and_equip_panel(screen, left_x + panel_width + padding, panel_y, panel_width, panel_height, 
                                             potion_data, small_font, self.potion_buttons)
            
            # Right side: stats and monster skills
            right_x = SCREEN_WIDTH - 2 * panel_width - padding - 30
            self._draw_info_panel(screen, right_x, panel_y, panel_width, panel_height, 
                                 "PLAYER STATS", player_stats_data, small_font)
            self._draw_info_panel(screen, right_x + panel_width + padding, panel_y, panel_width, panel_height, 
                                 "MONSTER SKILLS", monster_skills_data, small_font)

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
    
    def _draw_info_panel(self, screen, x, y, width, height, title, data, font):
        """Draws a single info panel."""
        # Draw panel background
        panel_surface = pygame.Surface((width, height))
        panel_surface.fill((30, 30, 30))
        panel_surface.set_alpha(200)
        screen.blit(panel_surface, (x, y))
        
        # Draw border
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height), 2)
        
        # Draw title
        title_surface = font.render(title, True, GOLD)
        title_rect = title_surface.get_rect(center=(x + width // 2, y + 8))
        screen.blit(title_surface, title_rect)
        
        # Draw content
        content_y = y + 25
        for line in data:
            if line.strip():
                line_surface = font.render(line, True, WHITE)
                screen.blit(line_surface, (x + 5, content_y))
            content_y += font.get_height() + 2
    
    def _get_player_skills(self):
        """Get player skills as list of strings."""
        skills = self.player.race.get_skills_dict() if hasattr(self.player.race, 'get_skills_dict') else []
        if not skills:
            return ["No skills"]
        result = []
        for skill in skills:
            result.append(f"• {skill}")
        return result
    
    def _get_monster_skills(self):
        """Get monster skills as list of strings."""
        skills = self.monster.race.get_skills_dict() if hasattr(self.monster, 'race') and hasattr(self.monster.race, 'get_skills_dict') else []
        if not skills:
            return ["No skills"]
        result = []
        for skill in skills:
            result.append(f"• {skill}")
        return result
    
    def _get_potion_and_equip_info(self):
        """Get potion count and equipped weapon."""
        result = []
        
        # Count potions in quick slots
        potion_count = sum(1 for item in self.player.equipment.quick_slots if item and item.item_type == "potion")
        
        # Count potions in inventory
        potion_count += sum(1 for item in self.player.inventory if item.item_type == "potion")
        
        result.append(f"Potions: {potion_count}")
        
        # Show equipped weapon
        if self.player.equipment.weapon:
            result.append(f"Weapon: {self.player.equipment.weapon.name}")
        else:
            result.append("Weapon: None")
        
        # Show equipped armor
        if self.player.equipment.armor:
            result.append(f"Armor: {self.player.equipment.armor.name}")
        else:
            result.append("Armor: None")
        
        return result
    
    def _get_player_stats(self):
        """Get player key statistics."""
        return [
            f"Level: {self.player.level}",
            f"Attack: {self.player.attack_power}",
            f"STR: {self.player.attribute_strength}",
            f"DEX: {self.player.attribute_dexterity}",
            f"INT: {self.player.attribute_intelligence}",
            f"WIS: {self.player.attribute_wisdom}",
            f"CHA: {self.player.attribute_charisma}",
            f"CON: {self.player.attribute_constitution}",
        ]
    
    def _calculate_panel_height(self, font, line_count):
        """Calculate dynamic panel height based on content."""
        title_height = 25
        line_height = font.get_height() + 2
        padding = 15
        min_height = 80
        
        calculated_height = title_height + (line_count * line_height) + padding
        return max(calculated_height, min_height)
    
    def _draw_info_panel(self, screen, x, y, width, height, title, data, font):
        """Draws a single info panel with dynamic height."""
        # Draw panel background
        panel_surface = pygame.Surface((width, height))
        panel_surface.fill((30, 30, 30))
        panel_surface.set_alpha(200)
        screen.blit(panel_surface, (x, y))
        
        # Draw border
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height), 2)
        
        # Draw title
        title_surface = font.render(title, True, GOLD)
        title_rect = title_surface.get_rect(center=(x + width // 2, y + 8))
        screen.blit(title_surface, title_rect)
        
        # Draw content
        content_y = y + 25
        for line in data:
            if line.strip():
                line_surface = font.render(line, True, WHITE)
                screen.blit(line_surface, (x + 5, content_y))
            content_y += font.get_height() + 2
    
    def _draw_potion_and_equip_panel(self, screen, x, y, width, height, data, font, potion_buttons):
        """Draws potion/equipment panel with clickable potion buttons."""
        # Draw panel background
        panel_surface = pygame.Surface((width, height))
        panel_surface.fill((30, 30, 30))
        panel_surface.set_alpha(200)
        screen.blit(panel_surface, (x, y))
        
        # Draw border
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height), 2)
        
        # Draw title
        title_surface = font.render("POTIONS/EQUIP", True, GOLD)
        title_rect = title_surface.get_rect(center=(x + width // 2, y + 8))
        screen.blit(title_surface, title_rect)
        
        # Separate potions from equipment
        potion_lines = []
        equip_lines = []
        
        for line in data:
            if "Potion" in line:
                # Count potions
                if line.startswith("Potions:"):
                    potion_lines.append(line)
            else:
                equip_lines.append(line)
        
        # Draw equipment info first
        content_y = y + 25
        for line in equip_lines:
            if line.strip():
                line_surface = font.render(line, True, WHITE)
                screen.blit(line_surface, (x + 5, content_y))
            content_y += font.get_height() + 2
        
        # Draw potion count
        if potion_lines:
            potion_count_text = potion_lines[0]
            line_surface = font.render(potion_count_text, True, GOLD)
            screen.blit(line_surface, (x + 5, content_y))
            content_y += font.get_height() + 4
        
        # Draw clickable potions from quick slots
        for i, potion_item in enumerate(self.player.equipment.quick_slots):
            if potion_item:
                button_height = 20
                button_y = content_y
                
                # Create button for this potion
                potion_button = Button(x + 5, button_y, width - 10, button_height, 
                                      f"Use: {potion_item.name}",
                                      action=lambda p=potion_item, idx=i: self.use_potion(p, quick_slot_index=idx),
                                      asset_manager=self.asset_manager)
                
                # Draw button
                potion_button.rect = pygame.Rect(x + 5, button_y, width - 10, button_height)
                pygame.draw.rect(screen, (100, 200, 100), potion_button.rect, 1)
                
                # Draw text
                potion_text = font.render(f"Use: {potion_item.name}", True, (150, 255, 150))
                screen.blit(potion_text, (x + 8, button_y + 3))
                
                potion_buttons.append(potion_button)
                content_y += button_height + 3