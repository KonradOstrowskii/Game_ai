# main_app/load_game_screen.py

import pygame
from button import Button
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class LoadGameScreen:
    """
    Screen for loading a previously saved game. Displays a list of save files.
    """
    def __init__(self, game, asset_manager):
        self.game = game
        self.asset_manager = asset_manager
        self.background = self.asset_manager.get_image('load_game')
        self.save_files = []
        self.save_buttons = []
        self.selected_save_file = None
        self.refresh_save_list()

        self.back_button = Button(50, 50, 150, 50, "Back",
                                  action=lambda: self.game.change_state('main_menu'))
        self.load_button = Button(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 100, 300, 70, "Load Game",
                                 action=self._load_selected_game)

    def refresh_save_list(self):
        """Refreshes the list of available save files and creates corresponding buttons."""
        self.save_files = self.game.get_all_save_files()
        self.save_buttons = []
        
        button_width = 400
        button_height = 60
        start_x = SCREEN_WIDTH / 2 - button_width / 2
        start_y = SCREEN_HEIGHT / 2 - 150
        spacing = 70

        for i, filename in enumerate(self.save_files):
            player_name = os.path.splitext(filename)[0].replace("player_", "")
            button = Button(start_x, start_y + i * spacing, button_width, button_height, 
                            player_name, action=self.create_select_save_action(filename))
            self.save_buttons.append(button)

    def create_select_save_action(self, filename):
        """Helper to create a closure for button action to select a save file."""
        def action():
            self.selected_save_file = filename
            for btn in self.save_buttons:
                btn.is_selected = (btn.text == os.path.splitext(filename)[0].replace("player_", ""))
        return action

    def _load_selected_game(self):
        """Loads the game from the currently selected save file."""
        if self.selected_save_file:
            loaded_player = self.game.load_player_from_json(self.selected_save_file)
            if loaded_player:
                self.game.player = loaded_player
                self.game.change_state('game_world')
            else:
                self.game.message = "Failed to load game."
        else:
            self.game.message = "No game selected."

    def handle_events(self, events):
        """Handles user input events for this screen."""
        for event in events:
            self.back_button.handle_event(event)
            self.load_button.handle_event(event)
            for button in self.save_buttons:
                button.handle_event(event)

    def draw(self, screen):
        """Draws the load game screen elements."""
        screen.blit(self.background, (0, 0))
        self.game.draw_text("Load Game", 'title', WHITE, SCREEN_WIDTH / 2, 100)
        
        font_medium = self.asset_manager.get_font('medium')

        if not self.save_files:
            self.game.draw_text("No saved games found.", 'large', BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        else:
            for button in self.save_buttons:
                button.draw(screen, font_medium)
            
            if self.selected_save_file:
                selected_name = os.path.splitext(self.selected_save_file)[0].replace("player_", "")
                self.game.draw_text(f"Selected: {selected_name}", 'medium', BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)

        self.back_button.draw(screen, font_medium)
        self.load_button.draw(screen, font_medium)