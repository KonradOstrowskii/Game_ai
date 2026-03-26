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
        self._load_image_scaled('main_menu', MENU_BACKGROUND_IMAGE)
        self._load_image_scaled('character_creation', CHARACTER_CREATION_BACKGROUND_IMAGE)
        self._load_image_scaled('load_game', LOAD_GAME_BACKGROUND_IMAGE)
        self._load_image_scaled('game_world', GAME_WORLD_BACKGROUND_IMAGE)
        # We can also load smaller, unscaled images here if needed
        # ### NEW: Changed from os.path.join to direct constant ###
        self._load_image_unscaled('input_box_bg', INPUT_BOX_BACKGROUND)
        print("Images loaded successfully.")

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

    def get_image(self, key):
        """Retrieves a pre-loaded image."""
        return self.images.get(key)

    def get_font(self, size_key):
        """Retrieves a pre-loaded font."""
        return self.fonts.get(size_key)