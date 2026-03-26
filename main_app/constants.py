# main_app/constants.py

import os

# Screen dimensions
# NOTE: UI layout is hardcoded for 1280x800. All button positions and text placement
# assume this exact screen size. Changing these values will break UI positioning.
# If responsive UI is needed in the future, button positions must be refactored.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
ACTIVE_COLOR = (150, 150, 150)
GOLD = (255, 215, 0)
TEXT_SHADOW_COLOR = (30, 30, 30) # For text shadows

# NEW / CORRECTED CONSTANTS FOR BUTTONS
BUTTON_TEXT_COLOR = WHITE
HOVER_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 165, 0) # Orange for selected buttons

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "assets")
SAVES_PATH = os.path.join(BASE_DIR, "saves")
PLAYER_DATA_PATH = os.path.join(ASSETS_PATH, "player_data")
ITEM_ICONS_PATH = os.path.join(ASSETS_PATH, "item_icons")

# Font configuration
FONT_PATH = os.path.join(ASSETS_PATH, "fonts", "MedievalSharp-Regular.ttf")


# Background images
# ### ZMIANY: Poprawione nazwy plików i rozszerzenia ###
MENU_BACKGROUND_IMAGE = os.path.join(ASSETS_PATH, "background_main_menu.jpg") # Zmieniono nazwę
CHARACTER_CREATION_BACKGROUND_IMAGE = os.path.join(ASSETS_PATH, "character_creation_background.png") # Zmieniono rozszerzenie na .png
LOAD_GAME_BACKGROUND_IMAGE = os.path.join(ASSETS_PATH, "load_game_background.png") # Zmieniono rozszerzenie na .png
GAME_WORLD_BACKGROUND_IMAGE = os.path.join(ASSETS_PATH, "game_world_background.png") # Zmieniono rozszerzenie na .png

# UI Elements
INPUT_BOX_BACKGROUND = os.path.join(ASSETS_PATH, "input_box_background.png") 

# Game World Screen Specifics
GAME_WORLD_PLAYER_CARD_X = SCREEN_WIDTH - 200 # X position for player card
GAME_WORLD_PLAYER_CARD_Y_START = 50 # Y start position for player card
GAME_WORLD_PLAYER_NAME_FONT_SIZE = 36 # Specific font size for player name
GAME_WORLD_PLAYER_STATS_FONT_SIZE = 24 # Specific font size for player stats
GAME_WORLD_STATS_Y_OFFSET = 50 # Y offset for stats lines