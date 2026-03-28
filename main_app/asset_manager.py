# main_app/asset_manager.py

import pygame
import os
from constants import (
    FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, DARK_GRAY, ASSETS_PATH, # ### ZMIANA 2: Import FONT_PATH ###
    MENU_BACKGROUND_IMAGE, CHARACTER_CREATION_BACKGROUND_IMAGE,
    LOAD_GAME_BACKGROUND_IMAGE, GAME_WORLD_BACKGROUND_IMAGE,
    INPUT_BOX_BACKGROUND # ### NEW: Import INPUT_BOX_BACKGROUND path
)

class AssetManager:
    """
    A class to manage loading and storing all game assets, such as images and fonts.
    This prevents reloading assets from disk multiple times.
    """
    def __init__(self):
        """
        Initializes the AssetManager and pre-loads all assets.
        """
        self.images = {}
        self.fonts = {}
        self._load_all()

    def _load_all(self):
        """Private helper method to load all assets at once."""
        self._load_fonts()
        self._load_images()

    def _load_fonts(self):
        """Pre-loads all the necessary fonts for the game."""
        # ### ZMIANA 3: Ładowanie czcionek z FONT_PATH ###
        # Używamy FONT_PATH bezpośrednio, co pozwala na ładowanie niestandardowych czcionek.
        # Wcześniej było pygame.font.match_font(FONT_NAME), co szukało czcionki w systemie.
        try:
            self.fonts['small'] = pygame.font.Font(FONT_PATH, 24)
            self.fonts['medium'] = pygame.font.Font(FONT_PATH, 32)
            self.fonts['large'] = pygame.font.Font(FONT_PATH, 38)
            self.fonts['title'] = pygame.font.Font(FONT_PATH, 64)
            print("Fonts loaded successfully.")
        except FileNotFoundError:
            print(f"Error: Font file not found at {FONT_PATH}. Using default Pygame font.")
            self.fonts['small'] = pygame.font.Font(None, 24)
            self.fonts['medium'] = pygame.font.Font(None, 32)
            self.fonts['large'] = pygame.font.Font(None, 38)
            self.fonts['title'] = pygame.font.Font(None, 64)
        except Exception as e:
            print(f"An unexpected error occurred while loading fonts: {e}. Using default Pygame font.")
            self.fonts['small'] = pygame.font.Font(None, 24)
            self.fonts['medium'] = pygame.font.Font(None, 32)
            self.fonts['large'] = pygame.font.Font(None, 38)
            self.fonts['title'] = pygame.font.Font(None, 64)


    def _load_images(self):
        """Pre-loads all the necessary images for the game."""
        # Temporarily disabled background images - using placeholders instead
        # self._load_image_scaled('main_menu', MENU_BACKGROUND_IMAGE)
        # self._load_image_scaled('character_creation', CHARACTER_CREATION_BACKGROUND_IMAGE)
        # self._load_image_scaled('load_game', LOAD_GAME_BACKGROUND_IMAGE)
        # self._load_image_scaled('game_world', GAME_WORLD_BACKGROUND_IMAGE)
        # self._load_image_unscaled('input_box_bg', INPUT_BOX_BACKGROUND)
        
        # Use Munchkin-style graphics instead of placeholders
        self._create_munchkin_graphics()
        
    def _create_munchkin_graphics(self):
        """Creates Munchkin-style graphics programmatically."""
        # Main menu background - bright and colorful
        self.images['main_menu'] = self._create_main_menu_bg()
        
        # Character creation background
        self.images['character_creation'] = self._create_character_creation_bg()
        
        # Game world background
        self.images['game_world'] = self._create_game_world_bg()
        
        # Load game background
        self.images['load_game'] = self._create_load_game_bg()
        
        # Input box background
        self.images['input_box_bg'] = self._create_input_box_bg()
        
        # Player card panel
        self.images['player_card'] = self._create_player_card()
        
        # Monster card panel
        self.images['monster_card'] = self._create_monster_card()
        
        # Button backgrounds
        self.images['button_normal'] = self._create_button_normal()
        self.images['button_hover'] = self._create_button_hover()
        self.images['button_selected'] = self._create_button_selected()
        
        # Item icons
        self._create_item_icons()

    def _create_main_menu_bg(self):
        """Creates a Munchkin-style main menu background."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Bright gradient background (yellow to orange)
        for y in range(SCREEN_HEIGHT):
            r = int(min(255, max(0, 255 - y // 3)))
            g = int(min(255, max(0, 200 - y // 4)))
            b = int(min(255, max(0, 100 - y // 8)))
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Add some Munchkin-style decorations
        self._draw_munchkin_decorations(surface, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        return surface

    def _create_character_creation_bg(self):
        """Creates character creation background with panels."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Light blue background
        surface.fill((135, 206, 235))  # Sky blue
        
        # Draw parchment-style panels
        self._draw_parchment_panel(surface, 50, 100, 400, 600, (255, 248, 220))  # Race selection
        self._draw_parchment_panel(surface, 500, 100, 400, 600, (255, 248, 220))  # Character preview
        
        return surface

    def _create_game_world_bg(self):
        """Creates game world background with player and action panels."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Forest green background
        surface.fill((34, 139, 34))  # Forest green
        
        return surface

    def _create_load_game_bg(self):
        """Creates load game background."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Purple background
        surface.fill((147, 112, 219))  # Medium purple
        
        # Draw save file panels
        for i in range(5):
            y = 100 + i * 120
            self._draw_parchment_panel(surface, 200, y, 800, 100, (255, 248, 220))
        
        return surface

    def _create_input_box_bg(self):
        """Creates input box background."""
        surface = pygame.Surface((380, 100))
        surface.fill((255, 255, 255))
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 3)  # Thick black border
        return surface

    def _create_player_card(self):
        """Creates a player card panel."""
        surface = pygame.Surface((300, 400))
        
        # Card background
        surface.fill((255, 248, 220))  # Parchment color
        pygame.draw.rect(surface, (139, 69, 19), surface.get_rect(), 4)  # Brown border
        
        # Title area
        pygame.draw.rect(surface, (255, 215, 0), (10, 10, 280, 40))  # Gold title bar
        pygame.draw.rect(surface, (0, 0, 0), (10, 10, 280, 40), 2)   # Black border
        
        # Stats area
        pygame.draw.rect(surface, (240, 240, 240), (10, 60, 280, 200))  # Light gray stats
        pygame.draw.rect(surface, (0, 0, 0), (10, 60, 280, 200), 2)
        
        # Equipment area
        pygame.draw.rect(surface, (220, 220, 220), (10, 270, 280, 120))  # Equipment
        pygame.draw.rect(surface, (0, 0, 0), (10, 270, 280, 120), 2)
        
        return surface

    def _create_monster_card(self):
        """Creates a monster card panel."""
        surface = pygame.Surface((300, 400))
        
        # Card background - red tint for monsters
        surface.fill((255, 240, 240))  # Light red
        pygame.draw.rect(surface, (139, 0, 0), surface.get_rect(), 4)  # Dark red border
        
        # Monster image area
        pygame.draw.rect(surface, (255, 200, 200), (10, 10, 280, 200))  # Monster art area
        pygame.draw.rect(surface, (139, 0, 0), (10, 10, 280, 200), 3)
        
        # Stats area
        pygame.draw.rect(surface, (240, 240, 240), (10, 220, 280, 170))  # Stats
        pygame.draw.rect(surface, (0, 0, 0), (10, 220, 280, 170), 2)
        
        return surface

    def _create_button_normal(self):
        """Creates normal button background."""
        surface = pygame.Surface((300, 70))
        surface.fill((100, 149, 237))  # Cornflower blue
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 3)  # Thick black border
        return surface

    def _create_button_hover(self):
        """Creates hover button background."""
        surface = pygame.Surface((300, 70))
        surface.fill((255, 255, 0))  # Yellow
        pygame.draw.rect(surface, (255, 0, 0), surface.get_rect(), 3)  # Red border
        return surface

    def _create_button_selected(self):
        """Creates selected button background."""
        surface = pygame.Surface((300, 70))
        surface.fill((255, 165, 0))  # Orange
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 4)  # Extra thick border
        return surface

    def _draw_parchment_panel(self, surface, x, y, width, height, color):
        """Draws a parchment-style panel with border."""
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, color, panel_rect)
        pygame.draw.rect(surface, (139, 69, 19), panel_rect, 3)  # Brown border
        
        # Add some texture lines for parchment effect
        for i in range(3):
            line_y = y + 20 + i * 15
            if line_y < y + height - 20:
                pygame.draw.line(surface, (222, 184, 135), (x + 10, line_y), (x + width - 10, line_y), 1)

    def _draw_munchkin_decorations(self, surface, width, height):
        """Draws Munchkin-style decorative elements."""
        # Draw some random geometric shapes
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        
        for i in range(20):
            color = colors[i % len(colors)]
            x = (i * 67) % width
            y = (i * 43) % height
            size = 20 + (i % 30)
            
            if i % 4 == 0:
                pygame.draw.circle(surface, color, (x, y), size // 2)
            elif i % 4 == 1:
                pygame.draw.rect(surface, color, (x, y, size, size))
            elif i % 4 == 2:
                points = [(x, y), (x + size, y + size//2), (x, y + size)]
                pygame.draw.polygon(surface, color, points)
            else:
                pygame.draw.ellipse(surface, color, (x, y, size, size//2))

    def _load_image_scaled(self, key, path):
        """Loads an image and scales it to the full screen size."""
        try:
            image = pygame.image.load(path).convert()
            self.images[key] = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Warning: Could not load and scale image at {path}: {e}")
            self.images[key] = self._create_placeholder(SCREEN_WIDTH, SCREEN_HEIGHT)

    def _load_image_unscaled(self, key, path):
        """Loads an image without scaling it."""
        try:
            self.images[key] = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Warning: Could not load image at {path}: {e}")
            self.images[key] = self._create_placeholder(100, 100) # Default placeholder size

    def _create_placeholder(self, width, height):
        """Creates a gray placeholder surface for missing images."""
        placeholder = pygame.Surface((width, height))
        placeholder.fill(DARK_GRAY)
        return placeholder

    def _create_item_icons(self):
        """Creates Munchkin-style item icons programmatically."""
        icon_size = 32
        
        # Weapon icon - sword shape
        weapon_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.rect(weapon_icon, (192, 192, 192), (12, 8, 8, 20))  # Blade
        pygame.draw.rect(weapon_icon, (139, 69, 19), (10, 24, 12, 4))   # Handle
        self.images['weapon_icon'] = weapon_icon
        
        # Armor icon - shield shape
        armor_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.polygon(armor_icon, (0, 100, 0), [(16, 4), (26, 10), (26, 26), (16, 28), (6, 26), (6, 10)])  # Shield
        pygame.draw.circle(armor_icon, (255, 215, 0), (16, 16), 3)  # Center emblem
        self.images['armor_icon'] = armor_icon
        
        # Helmet icon - helmet shape
        helmet_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.arc(helmet_icon, (139, 69, 19), (8, 8, 16, 16), 0, 3.14, 3)  # Helmet dome
        pygame.draw.rect(helmet_icon, (139, 69, 19), (6, 20, 20, 6))  # Helmet base
        pygame.draw.line(helmet_icon, (139, 69, 19), (10, 8), (10, 6), 2)  # Plume
        self.images['helmet_icon'] = helmet_icon
        
        # Shield icon - kite shield
        shield_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.polygon(shield_icon, (0, 0, 139), [(16, 4), (24, 8), (24, 24), (16, 28), (8, 24), (8, 8)])  # Shield
        pygame.draw.line(shield_icon, (255, 255, 255), (12, 12), (20, 12), 2)  # Cross
        pygame.draw.line(shield_icon, (255, 255, 255), (16, 8), (16, 20), 2)
        self.images['shield_icon'] = shield_icon
        
        # Accessory icon - ring shape
        accessory_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.circle(accessory_icon, (255, 215, 0), (16, 16), 8, 3)  # Ring
        pygame.draw.circle(accessory_icon, (255, 215, 0), (16, 16), 4)     # Gem
        self.images['accessory_icon'] = accessory_icon
        
        # Potion icon - bottle shape
        potion_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.rect(potion_icon, (0, 100, 0), (12, 8, 8, 16))  # Bottle
        pygame.draw.rect(potion_icon, (139, 69, 19), (14, 6, 4, 4))  # Cork
        pygame.draw.circle(potion_icon, (255, 0, 0), (16, 18), 2)    # Liquid
        self.images['potion_icon'] = potion_icon
        
        # Scroll icon - rolled paper
        scroll_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.rect(scroll_icon, (222, 184, 135), (8, 12, 16, 12))  # Paper
        pygame.draw.line(scroll_icon, (139, 69, 19), (8, 14), (8, 22), 1)  # Lines
        pygame.draw.line(scroll_icon, (139, 69, 19), (8, 16), (22, 16), 1)
        pygame.draw.line(scroll_icon, (139, 69, 19), (8, 18), (22, 18), 1)
        pygame.draw.line(scroll_icon, (139, 69, 19), (8, 20), (22, 20), 1)
        self.images['scroll_icon'] = scroll_icon
        
        # Consumable icon - bomb shape
        consumable_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        pygame.draw.circle(consumable_icon, (139, 69, 19), (16, 16), 6)  # Bomb body
        pygame.draw.line(consumable_icon, (139, 69, 19), (16, 10), (16, 6), 2)  # Fuse
        pygame.draw.circle(consumable_icon, (255, 0, 0), (16, 6), 1)    # Spark
        self.images['consumable_icon'] = consumable_icon

    def get_image(self, key):
        """Retrieves a pre-loaded image."""
        return self.images.get(key)

    def get_font(self, size_key):
        """Retrieves a pre-loaded font."""
        return self.fonts.get(size_key)