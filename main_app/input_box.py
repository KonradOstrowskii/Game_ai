# main_app/input_box.py

import pygame
from constants import DARK_GRAY, ACTIVE_COLOR, BLACK

class InputBox:
    """
    A class for a user input text box that can use a background image.
    """
    def __init__(self, x, y, width, height, text='', font=None, background_image=None, draw_background=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White background
        self.text = text
        
        if font is None:
            self.font = pygame.font.Font(None, 32)
        else:
            self.font = font
            
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        self.text_color = BLACK
        self.draw_background = draw_background  # Control whether to draw background image

        self.background_image = background_image
        if self.background_image and draw_background:
            self.background_image = pygame.transform.scale(self.background_image, (width, height))


    def handle_event(self, event):
        """
        Handles events for the input box, such as clicking to activate and typing.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = ACTIVE_COLOR if self.active else DARK_GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = DARK_GRAY
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.text_color)

    def draw(self, screen):
        """
        Draws the input box on the screen, with optional background image.
        """
        # Draw white background
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        
        # Draw background image if enabled
        if self.background_image and self.draw_background:
            screen.blit(self.background_image, self.rect.topleft)
        
        # Draw border
        border_color = ACTIVE_COLOR if self.active else (0, 0, 0)
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        # Draw text
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)