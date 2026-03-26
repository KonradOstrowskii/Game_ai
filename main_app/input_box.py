# main_app/input_box.py

import pygame
from constants import DARK_GRAY, ACTIVE_COLOR, BLACK

class InputBox:
    """
    A class for a user input text box that can use a background image.
    """
    def __init__(self, x, y, width, height, text='', font=None, background_image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DARK_GRAY
        self.text = text
        
        # ### ZMIANA 1: Używamy przekazanej czcionki ###
        # Zamiast tworzyć własną czcionkę, teraz używamy tej, którą dostaliśmy.
        # Jeśli z jakiegoś powodu czcionka nie zostanie podana, tworzymy domyślną.
        if font is None:
            self.font = pygame.font.Font(None, 32)
        else:
            self.font = font
            
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        self.text_color = BLACK

        # ### ZMIANA 2: Używamy przekazanej grafiki tła ###
        # Ta linijka już tu była, ale teraz jest w pełni funkcjonalna
        self.background_image = background_image
        if self.background_image:
            # Dopasowujemy rozmiar obrazka do naszego pola, jeśli nie jest już dopasowany
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
        Draws the input box on the screen, using a background image if provided.
        """
        if self.background_image:
            screen.blit(self.background_image, self.rect.topleft)
            if self.active:
                pygame.draw.rect(screen, ACTIVE_COLOR, self.rect, 3, border_radius=5)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 2)
        
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)