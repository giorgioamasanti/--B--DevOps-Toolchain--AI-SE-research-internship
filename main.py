import pygame
from tetris_game import TetrisGame

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Initialize the mixer for sound
    pygame.mixer.init()  # Add this line to initialize the mixer

    # Create an instance of TetrisGame
    game = TetrisGame()

    # Run the game
    game.run()