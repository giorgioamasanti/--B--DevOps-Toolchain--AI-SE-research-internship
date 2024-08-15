import pygame
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Grid:
    def __init__(self, width=10, height=20, block_size=30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.color_grid = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]  # New grid for colors

        # Ensure mixer is initialized before loading sounds
        pygame.mixer.init()

        # Load sound effect for tetromino placement
        self.tetromino_place_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/solidify.mp3'))

        # Load sound effect for row clearing
        self.row_clear_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/row_clear.mp3'))

        # Load sound effect for game over
        game_over_sound_path = os.path.join(os.path.dirname(__file__), 'assets/game_over.mp3')
        logging.info(f"Loading game over sound from: {game_over_sound_path}")  # Log the path being loaded
        if not os.path.exists(game_over_sound_path):
            logging.error(f"Error: Game over sound file does not exist at {game_over_sound_path}")  # Log if the file does not exist
        try:
            self.game_over_sound = pygame.mixer.Sound(game_over_sound_path)  # Load sound effect for game over
            logging.info("Game over sound loaded successfully.")
        except pygame.error as e:
            logging.error(f"Error loading game over sound: {e}", exc_info=True)  # Log any error that occurs while loading the sound

        logging.info("Tetromino placement sound, row clear sound, and game over sound loaded successfully")  # Log sound loading

        self.sound_effects_enabled = True  # Initialize sound effects state to enabled

    def draw(self, surface):
        surface.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                if self.grid[y][x] == 0:
                    pygame.draw.rect(surface, (200, 200, 200), rect, 1)  # Draw empty block outline in grey
                else:
                    pygame.draw.rect(surface, self.color_grid[y][x], rect)  # Draw filled block with its original color

    def reset(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.color_grid = [[(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]  # Reset color grid

    def is_full(self):
        return any(self.grid[0])  # Check if the top row is filled

    def place_tetromino(self, tetromino, position, sound_effects_enabled=True):
        shape = tetromino.get_shape()
        color = tetromino.get_color()  # Get the color of the tetromino
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block:  # If the block is part of the tetromino
                    if 0 <= position[0] + y < self.height and 0 <= position[1] + x < self.width:
                        self.grid[position[0] + y][position[1] + x] = 1  # Mark the grid as filled
                        self.color_grid[position[0] + y][position[1] + x] = color  # Store the color
                    else:
                        logging.warning(f"Tetromino position {position} is out of bounds.")
                        return 0  # Handle out-of-bounds gracefully
        filled_rows = self.clear_filled_rows(sound_effects_enabled)  # Clear filled rows after placing a tetromino
        if sound_effects_enabled:  # Check if sound effects are enabled before playing sound
            self.tetromino_place_sound.play()  # Play sound effect when tetromino is placed
        logging.info(f"place_tetromino: Filled rows cleared: {filled_rows}")  # Log for filled rows
        return filled_rows  # Return the number of filled rows cleared

    def is_valid_position(self, tetromino, position):
        shape = tetromino.get_shape()
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block:  # If the block is part of the tetromino
                    new_x = position[1] + x
                    new_y = position[0] + y
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False  # Out of bounds
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False  # Overlapping with another tetromino
        return True

    def get_state(self):
        """Return the current state of the grid."""
        return self.grid  # Return the grid state for rotation logic

    def rotate_tetromino(self, tetromino):
        """Rotate the tetromino and check for valid position."""
        original_shape = tetromino.get_shape()  # Backup the original shape
        if tetromino.rotate(self.get_state()):
            if not self.is_valid_position(tetromino, self.tetromino_position):
                logging.warning("Rotation resulted in invalid position, reverting.")
                tetromino.shape = original_shape  # Revert to original shape if invalid
                return False
            logging.info("Tetromino rotated successfully.")
            return True
        else:
            logging.warning("Rotation failed, shape remains unchanged.")
            return False

    def check_filled_rows(self):
        filled_rows = []
        for y in range(self.height):
            if all(self.grid[y]):  # Check if all columns in the row are filled
                filled_rows.append(y)  # Add the filled row index to the list
        logging.info(f"check_filled_rows: Filled rows detected: {filled_rows}")  # Log for filled rows
        return filled_rows

    def clear_filled_rows(self, sound_effects_enabled=True):
        filled_rows = self.check_filled_rows()  # Get filled rows
        for row in filled_rows:
            self.grid.pop(row)  # Remove the filled row
            self.grid.insert(0, [0 for _ in range(self.width)])  # Add a new empty row at the top
            self.color_grid.pop(row)  # Remove the color row
            self.color_grid.insert(0, [(0, 0, 0) for _ in range(self.width)])  # Add new empty color row
        logging.info(f"clear_filled_rows: Cleared filled rows: {filled_rows}")  # Log for filled rows

        if filled_rows:  # Check if any rows were cleared
            if sound_effects_enabled:  # Check if sound effects are enabled before playing sound
                try:
                    self.row_clear_sound.play()  # Play sound effect for row clearing
                    logging.info("Row clear sound played successfully.")  # Log sound playing
                except Exception as e:
                    logging.error(f"Error playing row clear sound: {e}", exc_info=True)  # Log any error that occurs while playing sound
        return len(filled_rows)  # Return the number of cleared rows

    def play_game_over_sound(self):
        """Play the game over sound effect."""
        try:
            self.game_over_sound.play()  # Play sound effect for game over
            logging.info("Game over sound played successfully.")  # Log sound playing
        except Exception as e:
            logging.error(f"Error playing game over sound: {e}", exc_info=True)  # Log any error that occurs while playing sound

    def check_game_over(self, current_tetromino, tetromino_position):
        """Check if the game is over (i.e., if a new tetromino collides on spawn)."""
        if not self.is_valid_position(current_tetromino, tetromino_position):
            logging.info("Game Over: New tetromino cannot be placed.")
            self.play_game_over_sound()  # Play the game over sound
            return True
        return False