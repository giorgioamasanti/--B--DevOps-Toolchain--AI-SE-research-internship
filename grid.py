import pygame
import os

class Grid:
    def __init__(self, width=10, height=20, block_size=30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.color_grid = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]  # New grid for colors
        self.tetromino_place_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/solidify.mp3'))  # Load sound effect
        print("Tetromino placement sound loaded successfully")  # Log sound loading

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

    def place_tetromino(self, tetromino, position):
        shape = tetromino.get_shape()
        color = tetromino.get_color()  # Get the color of the tetromino
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block:  # If the block is part of the tetromino
                    if 0 <= position[0] + y < self.height and 0 <= position[1] + x < self.width:
                        self.grid[position[0] + y][position[1] + x] = 1  # Mark the grid as filled
                        self.color_grid[position[0] + y][position[1] + x] = color  # Store the color
                    else:
                        print(f"Tetromino position {position} is out of bounds.")
                        return 0  # Handle out-of-bounds gracefully
        filled_rows = self.clear_filled_rows()  # Clear filled rows after placing a tetromino
        self.tetromino_place_sound.play()  # Play sound effect when tetromino is placed
        print(f"place_tetromino: Filled rows cleared: {filled_rows}")  # Debug print for filled rows
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
                print("Rotation resulted in invalid position, reverting.")
                tetromino.shape = original_shape  # Revert to original shape if invalid
                return False
            print("Tetromino rotated successfully.")
            return True
        else:
            print("Rotation failed, shape remains unchanged.")
            return False

    def check_filled_rows(self):
        filled_rows = []
        for y in range(self.height):
            if all(self.grid[y]):  # Check if all columns in the row are filled
                filled_rows.append(y)  # Add the filled row index to the list
        print(f"check_filled_rows: Filled rows detected: {filled_rows}")  # Debug print for filled rows
        return filled_rows

    def clear_filled_rows(self):
        filled_rows = self.check_filled_rows()  # Get filled rows
        for row in filled_rows:
            self.grid.pop(row)  # Remove the filled row
            self.grid.insert(0, [0 for _ in range(self.width)])  # Add a new empty row at the top
            self.color_grid.pop(row)  # Remove the color row
            self.color_grid.insert(0, [(0, 0, 0) for _ in range(self.width)])  # Add new empty color row
        print(f"clear_filled_rows: Cleared filled rows: {filled_rows}")  # Debug print for filled rows
        return len(filled_rows)  # Return the number of cleared rows