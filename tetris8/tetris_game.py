import pygame
import sys
import traceback
from tetromino import Tetromino
from grid import Grid


class TetrisGame:
    def __init__(self, width=10, height=20, block_size=30):

        # Initialize Pygame
        pygame.init()

        # Constants
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.fps = 60

        # Setup the display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris8")

        # Create grid
        self.grid = Grid(width, height, block_size)

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Instantiate the Tetromino
        self.current_tetromino = Tetromino()
        self.tetromino_position = [0, width // 2 - 1]  # Start at the top of the grid

        print("Tetris game initialized.")

    def run(self):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move_tetromino(-1, 0)  # Move left
                        elif event.key == pygame.K_RIGHT:
                            self.move_tetromino(1, 0)  # Move right
                        elif event.key == pygame.K_DOWN:
                            self.move_tetromino(0, 1)  # Move down
                        elif event.key == pygame.K_UP:
                            self.rotate_tetromino()  # Rotate

                # Clear the screen
                self.screen.fill((0, 0, 0))  # Fill with black background

                # Draw the grid
                self.grid.draw(self.screen)

                # Draw the current tetromino
                self.draw_tetromino()

                # Update the display
                pygame.display.flip()
                self.clock.tick(self.fps)

            except Exception as e:
                print("An error occurred: ", e)
                traceback.print_exc()

        pygame.quit()
        print("Tetris game exited.")

    def draw_tetromino(self):
        shape = self.current_tetromino.get_shape()
        color = self.current_tetromino.get_color()
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block:  # If the block is part of the tetromino
                    rect = pygame.Rect((self.tetromino_position[1] + x) * 30,
                                       (self.tetromino_position[0] + y) * 30,
                                       30, 30)
                    pygame.draw.rect(self.screen, color, rect)

    def move_tetromino(self, dx, dy):
        new_position = [self.tetromino_position[0] + dy, self.tetromino_position[1] + dx]

        if self.grid.is_valid_position(self.current_tetromino, new_position):
            self.tetromino_position = new_position
            print(f"Moved tetromino to position: {self.tetromino_position}")
        else:
            if dy == 1:  # If moving down and collision occurs, place the tetromino
                try:
                    self.grid.place_tetromino(self.current_tetromino, self.tetromino_position)
                    self.current_tetromino = Tetromino()  # Create a new tetromino
                    self.tetromino_position = [0, self.grid.width // 2 - 1]  # Reset position
                    if not self.grid.is_valid_position(self.current_tetromino, self.tetromino_position):
                        print("Game Over: New tetromino cannot be placed.")
                        pygame.quit()
                        sys.exit()
                except ValueError as e:
                    print("Error placing tetromino: ", e)
                    traceback.print_exc()

    def rotate_tetromino(self):
        # Backup the current shape to revert in case of collision
        original_shape = self.current_tetromino.get_shape()

        # Rotate the tetromino with the current grid state
        self.current_tetromino.rotate(self.grid.get_state())

        # Check for collisions after rotation
        if not self.grid.is_valid_position(self.current_tetromino, self.tetromino_position):
            # If there is a collision, revert to the original shape
            self.current_tetromino.shape = original_shape
            print(f"Collision detected, reverting rotation. Current position: {self.tetromino_position}, Original shape: {original_shape}")
        else:
            print("Tetromino rotated successfully.")