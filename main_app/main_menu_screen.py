# main_app/main_menu_screen.py

import pygame
from button import Button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class MainMenuScreen:
    """
    Represents the main menu screen of the game.
    Allows navigation to character creation, loading a game, or quitting.
    """
    def __init__(self, game, asset_manager):
        self.game = game
        self.asset_manager = asset_manager
        self.background = self.asset_manager.get_image('main_menu')
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        """Helper method to create and position main menu buttons."""
        button_width = 300
        button_height = 70
        start_y = SCREEN_HEIGHT / 2 - 100
        spacing = 90

        self.buttons.append(Button(
            (SCREEN_WIDTH / 2) - (button_width / 2), start_y, button_width, button_height,
            "New Game", action=lambda: self.game.change_state('character_creation'),
            asset_manager=self.asset_manager
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH / 2) - (button_width / 2), start_y + spacing, button_width, button_height,
            "Load Game", action=lambda: self.game.change_state('load_game'),
            asset_manager=self.asset_manager
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH / 2) - (button_width / 2), start_y + 2 * spacing, button_width, button_height,
            "Quit", action=self.game.quit_game,
            asset_manager=self.asset_manager
        ))

    def handle_events(self, events):
        """Handles user input events for the main menu."""
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self, screen):
        """Draws the main menu screen."""
        screen.blit(self.background, (0, 0))
        self.game.draw_text("Munchkin RPG", 'title', WHITE, SCREEN_WIDTH / 2, 150)
        
        font_large = self.asset_manager.get_font('large')
        for button in self.buttons:
            button.draw(screen, font_large)