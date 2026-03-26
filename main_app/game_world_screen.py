# main_app/game_world_screen.py

import pygame
from button import Button
from constants import (
    BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, # <-- Import FONT_NAME
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
                                   action=self.start_fight)
        self.back_to_menu_button = Button(50, 50, 200, 60, "Back to Menu",
                                          action=lambda: self.game.change_state('main_menu'))

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

    def handle_events(self, events):
        """Handle all user input events for the screen."""
        for event in events:
            self.fight_button.handle_event(event)
            self.back_to_menu_button.handle_event(event)

    def draw(self, screen):
        """Draw the game world screen, including player stats and buttons."""
        screen.blit(self.background, (0, 0))

        if self.game.player:
            text_x = GAME_WORLD_PLAYER_CARD_X
            text_y_start = GAME_WORLD_PLAYER_CARD_Y_START

            # ### ZMIANA: Tworzymy nowe czcionki używając FONT_NAME z constants ###
            # Zamiast próbować .name, bezpośrednio tworzymy nowe obiekty czcionek
            # używając nazwy fontu z pliku konfiguracyjnego.
            font_path = pygame.font.match_font(FONT_PATH)
            font_name_custom = pygame.font.Font(font_path, GAME_WORLD_PLAYER_NAME_FONT_SIZE)
            font_stats_custom = pygame.font.Font(font_path, GAME_WORLD_PLAYER_STATS_FONT_SIZE)
            
            # Rysowanie tekstu przy użyciu nowo stworzonych, niestandardowych czcionek
            name_surface = font_name_custom.render(self.game.player.name, True, BLACK)
            name_rect = name_surface.get_rect(center=(text_x, text_y_start))
            screen.blit(name_surface, name_rect)

            player_stats_lines = str(self.game.player).split('\n')
            y_offset = text_y_start + GAME_WORLD_STATS_Y_OFFSET
            
            # Rysujemy tylko te linie, które chcemy (bez nazwy, bo jest już w tytule)
            for line in player_stats_lines[1:]: # Zaczynamy od drugiego elementu
                stats_surface = font_stats_custom.render(line, True, BLACK)
                stats_rect = stats_surface.get_rect(midtop=(text_x, y_offset))
                screen.blit(stats_surface, stats_rect)
                y_offset += font_stats_custom.get_height()
        else:
            self.game.draw_text("No player loaded or created.", 'medium', WHITE, SCREEN_WIDTH / 2, 250)

        self.fight_button.draw(screen, self.asset_manager.get_font('large'))
        self.back_to_menu_button.draw(screen, self.asset_manager.get_font('medium'))