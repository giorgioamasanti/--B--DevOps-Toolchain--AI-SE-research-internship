import pygame
import sys
import logging
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
        pygame.display.set_caption("Tetris")

        # Create grid
        self.grid = Grid(width, height, block_size)

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Instantiate the Tetromino
        self.current_tetromino = Tetromino()
        self.tetromino_position = [0, width // 2 - 1]  # Start at the top of the grid

        logging.info("Tetris game initialized.")

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
                logging.error("An error occurred: ", exc_info=True)

        pygame.quit()
        logging.info("Tetris game exited.")

    def draw_tetromino(self):
        if self.current_tetromino:  # Check if current tetromino is valid
            shape = self.current_tetromino.current_shape  # Use the current shape matrix
            color = self.current_tetromino.get_color()

            # Add a log to verify the shape being drawn
            logging.debug(f"Drawing Tetromino: shape: {shape}, color: {color}")

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
            logging.info(f"Moved tetromino to position: {self.tetromino_position}")
        else:
            if dy == 1:  # If moving down and collision occurs, place the tetromino
                try:
                    self.grid.place_tetromino(self.current_tetromino, self.tetromino_position)
                    self.current_tetromino = Tetromino()  # Create a new tetromino
                    self.tetromino_position = [0, self.grid.width // 2 - 1]  # Reset position
                    if not self.grid.is_valid_position(self.current_tetromino, self.tetromino_position):
                        logging.error("Game Over: New tetromino cannot be placed.")
                        pygame.quit()
                        sys.exit()
                except ValueError as e:
                    logging.error("Error placing tetromino: ", exc_info=True)

    def rotate_tetromino(self):
        original_shape = self.current_tetromino.current_shape  # Backup the original shape

        # Rotate the tetromino with the current grid state and position
        if self.current_tetromino.rotate(self.grid.get_state(), self.tetromino_position):
            # Check for collisions after rotation
            if not self.grid.is_valid_position(self.current_tetromino, self.tetromino_position):
                # If there is a collision, revert to the original shape
                self.current_tetromino.current_shape = original_shape
                logging.warning(f"Collision detected, reverting rotation. Current position: {self.tetromino_position}, Original shape: {original_shape}")
            else:
                logging.info("Tetromino rotated successfully.")
        else:
            logging.warning("Rotation failed, shape remains unchanged.")
