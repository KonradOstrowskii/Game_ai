# main_app/button.py

import pygame
from constants import (
    BUTTON_TEXT_COLOR, LIGHT_GRAY, HOVER_COLOR, SELECTED_COLOR, DARK_GRAY, # ### ZMIANA: Poprawione importy ###
    TEXT_SHADOW_COLOR
)

class Button:
    """
    A customizable button class for the Pygame GUI.
    """
    def __init__(self, x, y, width, height, text, action=None, color=DARK_GRAY, hover_color=HOVER_COLOR, asset_manager=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.asset_manager = asset_manager
        self.current_color = self.color
        self.is_selected = False # For toggle buttons, like race selection
        self.state = 'normal'  # normal, hover, selected

    def handle_event(self, event):
        """
        Handles mouse input for the button.
        """
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state = 'hover'
            else:
                self.state = 'selected' if self.is_selected else 'normal'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                # If it's a selectable button, toggle its selected state on click
                # This logic might need refinement depending on how buttons are used
                # For now, it will mark it selected and other buttons might unselect it
                if self.action and "create_race_selection_action" in str(self.action): # Crude check for race selection
                    self.is_selected = True # Mark this button as selected on click
        
    def draw(self, screen, font):
        """
        Draws the button on the screen with text.
        :param screen: The Pygame surface to draw on.
        :param font: The Pygame font object to use for the button text.
        """
        # Try to use Munchkin-style button graphics
        button_image = None
        if self.asset_manager:
            if self.state == 'hover':
                button_image = self.asset_manager.get_image('button_hover')
            elif self.state == 'selected':
                button_image = self.asset_manager.get_image('button_selected')
            else:
                button_image = self.asset_manager.get_image('button_normal')
        
        if button_image:
            # Scale the button image to fit our button size
            scaled_image = pygame.transform.scale(button_image, (self.rect.width, self.rect.height))
            screen.blit(scaled_image, self.rect)
        else:
            # Fallback to old drawing method
            current_fill_color = SELECTED_COLOR if self.is_selected else self.current_color
            pygame.draw.rect(screen, current_fill_color, self.rect, border_radius=5)
            pygame.draw.rect(screen, LIGHT_GRAY, self.rect, 3, border_radius=5) # Border

        # Draw text with shadow
        shadow_surface = font.render(self.text, True, TEXT_SHADOW_COLOR)
        shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        screen.blit(shadow_surface, shadow_rect)

        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)