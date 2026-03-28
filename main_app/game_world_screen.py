# main_app/game_world_screen.py

import pygame
from button import Button
from constants import (
    BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, LIGHT_GRAY, GOLD,
    GAME_WORLD_PLAYER_CARD_X, GAME_WORLD_PLAYER_CARD_Y_START,
    GAME_WORLD_PLAYER_NAME_FONT_SIZE, GAME_WORLD_PLAYER_STATS_FONT_SIZE,
    GAME_WORLD_STATS_Y_OFFSET
)

class GameWorldScreen:
    """
    The main game world screen where the player can see their stats and choose actions.
    """
    def __init__(self, game, asset_manager):
        self.game = game
        self.asset_manager = asset_manager
        self.background = self.asset_manager.get_image('game_world')
        self.fight_button = Button((SCREEN_WIDTH / 2) - 150, SCREEN_HEIGHT - 80, 300, 70, "Find Trouble!",
                                   action=self.start_fight, asset_manager=asset_manager)
        self.back_to_menu_button = Button(50, 50, 200, 60, "Back to Menu",
                                          action=lambda: self.game.change_state('main_menu'), asset_manager=asset_manager)

    def start_fight(self):
        """Starts a new fight if a player is loaded."""
        if self.game.player:
            if 'fight' in self.game.screens:
                self.game.screens['fight'].start_new_fight(self.game.player)
                self.game.change_state('fight')
            else:
                self.game.message = "Cannot start fight: Game setup error."
        else:
            self.game.message = "No player to fight with! Create or load one."

    def _get_stats_data(self):
        """Returns player stats data as a list of strings."""
        player = self.game.player
        return [
            f"Name: {player.name}",
            f"Level: {player.level}",
            f"Experience: {player.experience}",
            f"",
            f"Attack: {player.attack_power}",
            f"HP: {player.hit_points}/{player._hit_points_max}",
            f"",
            f"Strength: {player.attribute_strength}",
            f"Dexterity: {player.attribute_dexterity}",
            f"Intelligence: {player.attribute_intelligence}",
            f"Charisma: {player.attribute_charisma}",
            f"Wisdom: {player.attribute_wisdom}",
            f"Constitution: {player.attribute_constitution}"
        ]

    def _get_skills_data(self):
        """Returns player skills data as a list of strings."""
        player = self.game.player
        skills = player.race.get_skills_dict() if hasattr(player.race, 'get_skills_dict') else []
        
        if not skills:
            return ["No skills available"]
        
        result = []
        for skill in skills:
            result.append(f"• {skill}")
        return result

    def _get_equipment_data(self):
        """Returns player equipment data as a list of strings."""
        player = self.game.player
        equipment = player.equipment if hasattr(player, 'equipment') else None
        
        if not equipment:
            return ["No equipment equipped"]
        
        result = []
        
        # Check each equipment slot
        if equipment.weapon:
            result.append(f"Weapon: {equipment.weapon.name}")
        else:
            result.append("Weapon: Empty")
        
        if equipment.armor:
            result.append(f"Armor: {equipment.armor.name}")
        else:
            result.append("Armor: Empty")
        
        if equipment.helmet:
            result.append(f"Helmet: {equipment.helmet.name}")
        else:
            result.append("Helmet: Empty")
        
        if equipment.shield:
            result.append(f"Shield: {equipment.shield.name}")
        else:
            result.append("Shield: Empty")
        
        if equipment.accessory:
            result.append(f"Accessory: {equipment.accessory.name}")
        else:
            result.append("Accessory: Empty")
        
        return result

    def _get_inventory_data(self):
        """Returns player inventory data as a list of strings."""
        player = self.game.player
        inventory = player.inventory if hasattr(player, 'inventory') else []
        
        if not inventory:
            return ["Inventory empty"]
        
        result = [f"Items: {len(inventory)}/{player.max_inventory_slots}"]
        for item in inventory[:8]:  # Only show first 8 items to fit in panel
            result.append(f"• {item.name}")
        
        if len(inventory) > 8:
            result.append(f"... +{len(inventory) - 8} more")
        
        return result

    def _draw_panel(self, screen, position, width, height, title, data, font_title, font_content):
        """Draw a single panel with title and content."""
        x, y = position
        
        # Draw panel background (semi-transparent dark rectangle)
        panel_surface = pygame.Surface((width, height))
        panel_surface.fill((30, 30, 30))
        panel_surface.set_alpha(200)
        screen.blit(panel_surface, (x, y))
        
        # Draw panel border
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height), 2)
        
        # Draw title
        title_surface = font_title.render(title, True, GOLD)
        title_rect = title_surface.get_rect(center=(x + width // 2, y + 15))
        screen.blit(title_surface, title_rect)
        
        # Draw content
        content_y = y + 40
        for line in data:
            if line.strip():  # Skip empty lines for spacing
                line_surface = font_content.render(line, True, WHITE)
                screen.blit(line_surface, (x + 10, content_y))
            content_y += font_content.get_height() + 3

    def handle_events(self, events):
        """Handle all user input events for the screen."""
        for event in events:
            self.fight_button.handle_event(event)
            self.back_to_menu_button.handle_event(event)

    def draw(self, screen):
        """Draw the game world screen, including player stats and buttons."""
        screen.blit(self.background, (0, 0))

        if self.game.player:
            # Panel dimensions and positions (2x2 grid) - larger panels
            panel_width = 380
            panel_height = 320
            padding = 25
            start_x = 120  # Moved right
            start_y = 90   # Moved down to make room for back to menu
            
            # Panel positions: top-left, top-right, bottom-left, bottom-right
            positions = [
                (start_x, start_y),  # Stats (top-left)
                (start_x + panel_width + padding, start_y),  # Skills (top-right)
                (start_x, start_y + panel_height + padding),  # Equipment (bottom-left)
                (start_x + panel_width + padding, start_y + panel_height + padding)  # Inventory (bottom-right)
            ]
            
            titles = ["STATS", "SKILLS", "EQUIPMENT", "INVENTORY"]
            panels_data = [
                self._get_stats_data(),
                self._get_skills_data(),
                self._get_equipment_data(),
                self._get_inventory_data()
            ]
            
            font_path = pygame.font.match_font(FONT_PATH)
            font_title = pygame.font.Font(font_path, 22)
            font_content = pygame.font.Font(font_path, 15)
            
            # Draw all 4 panels
            for i, (pos, title, data) in enumerate(zip(positions, titles, panels_data)):
                self._draw_panel(screen, pos, panel_width, panel_height, title, data, font_title, font_content)
        else:
            self.game.draw_text("No player loaded or created.", 'medium', WHITE, SCREEN_WIDTH / 2, 250)

        self.fight_button.draw(screen, self.asset_manager.get_font('large'))
        self.back_to_menu_button.draw(screen, self.asset_manager.get_font('medium'))