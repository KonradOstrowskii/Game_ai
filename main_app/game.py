# main_app/game.py

import pygame
import sys
import os
# ### ZMIANA: Usunięto FONT_NAME z importu ###
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, RED, FPS, TEXT_SHADOW_COLOR, FONT_PATH, ASSETS_PATH
from asset_manager import AssetManager
from main_menu_screen import MainMenuScreen
from character_creation_screen import CharacterCreationScreen
from load_game_screen import LoadGameScreen
from game_world_screen import GameWorldScreen
from fight_screen import FightScreen
from post_fight_summary_screen import PostFightSummaryScreen
from inventory_screen import InventoryScreen
from characters.player import Player
from saving_data.save_and_load_player import save_player_to_json, load_player_from_json, get_all_save_files

class Game:
    """
    Main class for the Munchkin-like RPG Adventure game.
    Manages game states, main loop, resource loading, and global utilities.
    """
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Munchkin-like RPG Adventure")
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Validate required assets before initializing game
        self._validate_assets()

        self.asset_manager = AssetManager()

        self.Player = Player
        self.save_player_to_json = save_player_to_json
        self.load_player_from_json = load_player_from_json
        self.get_all_save_files = get_all_save_files

        self.state = 'main_menu'
        self.player = None
        self.screens = {}
        self._initialize_screens()
        self.current_screen = self.screens[self.state]
        self.message = ""
        self.last_fight_rewards = {}

    def _validate_assets(self):
        """
        Validates that required assets exist before starting the game.
        Since we now use programmatic graphics, only the font file is required.
        """
        required_files = [
            (FONT_PATH, "Font file (MedievalSharp-Regular.ttf)"),
        ]
        
        missing_assets = []
        for asset_path, asset_name in required_files:
            if not os.path.exists(asset_path):
                missing_assets.append(f"  - {asset_name}: {asset_path}")
        
        if missing_assets:
            error_msg = (
                "ERROR: Missing required game assets!\n\n"
                "The following files are required to run the game:\n"
                + "\n".join(missing_assets) +
                "\n\nPlease ensure the 'assets' folder contains all required files.\n"
                "See GETTING_STARTED.md for setup instructions."
            )
            print(error_msg)
            pygame.quit()
            sys.exit(1)
        
        print("✓ All required assets validated successfully.")

    def _initialize_screens(self):
        """Initializes all game screens and stores them in a dictionary."""
        self.screens = {
            'main_menu': MainMenuScreen(self, self.asset_manager),
            'character_creation': CharacterCreationScreen(self, self.asset_manager),
            'load_game': LoadGameScreen(self, self.asset_manager),
            'game_world': GameWorldScreen(self, self.asset_manager),
            'fight': FightScreen(self, self.asset_manager),
            'post_fight_summary': PostFightSummaryScreen(self, self.asset_manager),
            'inventory': InventoryScreen(self, self.asset_manager)
        }

    def run(self):
        """Starts the main game loop."""
        while self.is_running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        """Handles Pygame events for the current screen."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            if self.state == 'game_world' and event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.change_state('inventory')
                return
        self.current_screen.handle_events(events)

    def update(self):
        """Updates game logic for the current screen."""
        if self.state == 'load_game':
            self.current_screen.refresh_save_list()

    def draw(self):
        """Draws the current screen and any global elements."""
        self.current_screen.draw(self.screen)
        if self.message:
            # Używamy bezpośrednio asset_manager.get_font, nie potrzebujemy już FONT_NAME
            self.draw_text(self.message, 'medium', RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
        pygame.display.flip()

    def change_state(self, new_state):
        """Changes the current game state to a new screen."""
        if new_state in self.screens:
            self.state = new_state
            self.current_screen = self.screens[self.state]
            # Pass player to the inventory screen
            if new_state == 'inventory':
                self.current_screen.player = self.player
            self.message = ""
        else:
            print(f"Error: Unknown state '{new_state}'")

    def draw_text(self, text, size_key, color, x, y, center=True):
        """Draws text on the screen with a shadow, using pre-loaded fonts."""
        font_to_use = self.asset_manager.get_font(size_key)
        if not font_to_use:
            print(f"Warning: Font key '{size_key}' not found. Using default Pygame font.")
            # Jeśli czcionka nie zostanie znaleziona, używamy domyślnej Pygame
            font_to_use = pygame.font.Font(None, 32)
        
        lines = text.split('\n')
        y_offset = y

        for line in lines:
            shadow_surface = font_to_use.render(line, True, TEXT_SHADOW_COLOR)
            shadow_rect = shadow_surface.get_rect()
            shadow_pos = (x + 2, y_offset + 2)
            if center: shadow_rect.midtop = shadow_pos
            else: shadow_rect.topleft = shadow_pos
            self.screen.blit(shadow_surface, shadow_rect)

            text_surface = font_to_use.render(line, True, color)
            text_rect = text_surface.get_rect()
            if center: text_rect.midtop = (x, y_offset)
            else: text_rect.topleft = (x, y_offset)
            self.screen.blit(text_surface, text_rect)
            
            y_offset += font_to_use.get_height()

    def quit_game(self):
        """Sets the game state to stop the main loop."""
        self.is_running = False