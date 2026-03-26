# main_app/character_creation_screen.py

import pygame
import textwrap
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from button import Button
from input_box import InputBox
from characters.player import Player
from characters.creating_player import RACE_CONFIG
from saving_data.save_and_load_player import save_player_to_json

class CharacterCreationScreen:
    """
    Screen for creating a new character, allowing the player to enter a name and choose a race.
    """
    def __init__(self, game, asset_manager):
        self.game = game
        self.asset_manager = asset_manager
        self.background = self.asset_manager.get_image('character_creation')
        
        input_card_width = 380
        input_card_height = 100
        input_card_x = (SCREEN_WIDTH / 2) - (input_card_width / 2) + 10
        input_card_y = 660

        self.name_input = InputBox(
            input_card_x, input_card_y, 
            input_card_width, input_card_height,
            font=self.asset_manager.get_font('medium'),
            background_image=self.asset_manager.get_image('input_box_bg')
        )
        
        self.race_buttons = {}
        button_y_start = 380
        for key, config in RACE_CONFIG.items():
            race_name = config['class']().name
            button = Button(100, button_y_start, 250, 60, race_name,
                            action=self.create_race_selection_action(key))
            self.race_buttons[key] = button
            button_y_start += 80
        
        self.selected_race_key = None
        self.create_button = Button((SCREEN_WIDTH / 2) - 150, SCREEN_HEIGHT - 100, 300, 70, "Create Character",
                                    action=self.create_character)
        
        self.back_button = Button(50, 50, 150, 50, "Back", action=lambda: self.game.change_state('main_menu'))

    def create_race_selection_action(self, key):
        """Creates a dynamic action for race selection buttons."""
        def action():
            self.selected_race_key = key
            for other_key, other_button in self.race_buttons.items():
                other_button.is_selected = (key == other_key)
        return action

    def handle_events(self, events):
        """Handles user input events for this screen."""
        for event in events:
            self.name_input.handle_event(event)
            self.create_button.handle_event(event)
            self.back_button.handle_event(event)
            for button in self.race_buttons.values():
                button.handle_event(event)
    
    def create_character(self):
        """
        Validates input and creates a new player character.
        Checks:
        - Name is not empty or whitespace-only
        - Name is between 3 and 20 characters
        - A race has been selected
        """
        player_name = self.name_input.text.strip()
        
        # Validate name: not empty
        if not player_name:
            self.game.message = "Name cannot be empty!"
            return
        
        # Validate name length
        if len(player_name) < 3:
            self.game.message = "Name must be at least 3 characters!"
            return
        
        if len(player_name) > 20:
            self.game.message = "Name must be 20 characters or less!"
            return
        
        # Validate race selection
        if not self.selected_race_key:
            self.game.message = "Please select a race!"
            return

        player = Player(player_name) 
        config = RACE_CONFIG[self.selected_race_key]
        player.race = config["class"]()
        player.apply_race_bonuses()

        for item in config["items"]:
            player.equipment.equip(item)
        
        save_player_to_json(player)
        self.game.player = player
        self.game.change_state('game_world')

    def draw(self, screen):
        """Draws the character creation screen elements."""
        screen.blit(self.background, (0, 0))
        self.game.draw_text("Create Your Hero", 'title', WHITE, SCREEN_WIDTH / 2, 100)
        self.game.draw_text("Enter Your Name:", 'large', BLACK, SCREEN_WIDTH / 2, 620)
        self.name_input.draw(screen)
        
        self.game.draw_text("Choose Your Race:", 'large', BLACK, 225, 340)
        
        font_medium = self.asset_manager.get_font('medium')
        for button in self.race_buttons.values(): 
            button.draw(screen, font_medium)
        
        if self.selected_race_key:
            config = RACE_CONFIG[self.selected_race_key]
            race_instance = config['class']()
            papyrus_center_x = SCREEN_WIDTH // 2
            description_y_start = 320
            
            self.game.draw_text(f"--- {race_instance.name} ---", 'large', BLACK, papyrus_center_x, description_y_start)

            description_text = str(race_instance).strip().replace('\n', ' ')
            wrapped_lines = textwrap.wrap(description_text, width=50)
            y_offset = description_y_start + 50
            for line in wrapped_lines:
                self.game.draw_text(line, 'small', BLACK, papyrus_center_x, y_offset)
                y_offset += 30

        self.create_button.draw(screen, font_medium)
        self.back_button.draw(screen, font_medium)