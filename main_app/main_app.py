"""
Main entry point for the game.
This file creates a Game instance and runs it.
"""
import sys
import pygame
from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()