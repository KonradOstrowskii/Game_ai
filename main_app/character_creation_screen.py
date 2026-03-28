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
        
        # Name input
        input_card_width = 380
        input_card_height = 56
        input_card_x = SCREEN_WIDTH - input_card_width - 60
        input_card_y = SCREEN_HEIGHT - 140

        self.name_input = InputBox(
            input_card_x, input_card_y,
            input_card_width, input_card_height,
            font=self.asset_manager.get_font('medium'),
            background_image=self.asset_manager.get_image('input_box_bg'),
            draw_background=False  # Don't draw the background image, just clean border
        )
        self.input_card_y = input_card_y

        # Race selection buttons in left panel
        self.race_buttons = {}
        button_y_start = 200
        button_height = 60
        button_width = 300
        for key, config in RACE_CONFIG.items():
            race_name = config['class']().name
            button = Button(80, button_y_start, button_width, button_height, race_name,
                            action=self.create_race_selection_action(key), asset_manager=self.asset_manager)
            self.race_buttons[key] = button
            button_y_start += button_height + 16

        self.selected_race_key = None
        self.create_button = Button(SCREEN_WIDTH - 380 - 60, SCREEN_HEIGHT - 80, 380, 60, "Create Character",
                                    action=self.create_character, asset_manager=self.asset_manager)

        self.back_button = Button(50, 50, 150, 50, "Back", action=lambda: self.game.change_state('main_menu'), asset_manager=self.asset_manager)

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

        # Header
        self.game.draw_text("Create Your Hero", 'title', WHITE, SCREEN_WIDTH / 2, 50)

        # Large panels spanning most of screen
        left_panel = pygame.Rect(40, 110, 500, 640)
        right_panel = pygame.Rect(740, 110, 500, 640)
        pygame.draw.rect(screen, (255, 248, 220), left_panel)
        pygame.draw.rect(screen, (139, 69, 19), left_panel, 4)
        pygame.draw.rect(screen, (255, 248, 220), right_panel)
        pygame.draw.rect(screen, (139, 69, 19), right_panel, 4)

        # Left panel: Race selection
        self.game.draw_text("Choose Your Race:", 'large', BLACK, left_panel.centerx, left_panel.top + 20)

        font_medium = self.asset_manager.get_font('medium')
        for button in self.race_buttons.values():
            button.draw(screen, font_medium)

        # Right panel: Race description
        self.game.draw_text("Race Description", 'large', BLACK, right_panel.centerx, right_panel.top + 20)

        if self.selected_race_key:
            config = RACE_CONFIG[self.selected_race_key]
            race_instance = config['class']()

            desc_title = f"--- {race_instance.name} ---"
            self.game.draw_text(desc_title, 'medium', BLACK, right_panel.centerx, right_panel.top + 70)

            description_text = str(race_instance).strip().replace('\n', ' ')
            wrapped_lines = textwrap.wrap(description_text, width=40)
            y_offset = right_panel.top + 110
            max_desc_bottom = right_panel.bottom - 100
            font_small = self.asset_manager.get_font('small')
            for line in wrapped_lines:
                if y_offset > max_desc_bottom:
                    break
                text_surface = font_small.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(right_panel.centerx, y_offset))
                screen.blit(text_surface, text_rect)
                y_offset += 22
        else:
            self.game.draw_text("Select a race to see details.", 'small', BLACK, right_panel.centerx, right_panel.top + 150)

        # Bottom: Name input area (simplified, no background image)
        self.game.draw_text("Enter Your Name:", 'large', BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.name_input.draw(screen)

        # Action buttons
        self.create_button.draw(screen, font_medium)
        self.back_button.draw(screen, font_medium)