import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set to INFO to reduce noise in production

class Tetromino:
    shapes = {
        'I': [[1, 1, 1, 1]],
        'O': [[1, 1],
              [1, 1]],
        'T': [[0, 1, 0],
              [1, 1, 1]],
        'J': [[0, 0, 1],
              [1, 1, 1]],
        'L': [[1, 0, 0],
              [1, 1, 1]],
        'S': [[0, 1, 1],
              [1, 1, 0]],
        'Z': [[1, 1, 0],
              [0, 1, 1]]
    }

    colors = {
        'I': (0, 255, 255),  # Cyan
        'O': (255, 255, 0),  # Yellow
        'T': (128, 0, 128),  # Purple
        'J': (0, 0, 255),    # Blue
        'L': (255, 165, 0),  # Orange
        'S': (0, 255, 0),    # Green
        'Z': (255, 0, 0)     # Red
    }

    def __init__(self):
        self.shape = self.random_shape()
        self.color = self.colors[self.shape]
        self.current_shape = self.shapes[self.shape]  # Initialize current shape
        logging.debug(f"Tetromino created with shape: {self.shape} and color: {self.color}")

    def random_shape(self):
        shape = random.choice(list(self.shapes.keys()))
        logging.debug(f"DEBUG: Random shape selected: {shape}")
        return shape

    def get_shape(self):
        return self.current_shape  # Return the current shape matrix

    def get_color(self):
        return self.color

    def rotate(self, grid_state, position):
        logging.debug(f"Rotating Tetromino: current shape type before rotation: {self.shape}")

        rotated_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        logging.debug(f"Tetromino rotated to shape: {rotated_shape}")

        original_shape = self.current_shape  # Store the original shape matrix

        # Check for valid rotation
        if self.is_valid_rotation(rotated_shape, grid_state, position):
            logging.debug(f"Rotation valid for shape: {self.shape}, updating shape.")
            self.current_shape = rotated_shape  # Update current shape
            logging.info("Tetromino rotated successfully.")
            print(f"DEBUG: Tetromino rotated to shape: {self.current_shape}")
            return True  # Indicate successful rotation
        else:
            logging.warning("Rotation invalid, reverting to original shape.")
            self.current_shape = original_shape  # Restore original shape matrix
            print(f"DEBUG: Tetromino remained as shape: {self.current_shape}")
            return False  # Indicate failed rotation

    def is_valid_rotation(self, rotated_shape, grid_state, position):
        # Check for collisions with the grid boundaries and other tetrominoes
        for y, row in enumerate(rotated_shape):
            for x, block in enumerate(row):
                if block:  # If the block is part of the tetromino
                    new_x = position[1] + x
                    new_y = position[0] + y
                    # Check if the position is out of bounds
                    if new_x < 0 or new_x >= len(grid_state[0]) or new_y < 0 or new_y >= len(grid_state):
                        logging.warning("Collision with grid boundary detected.")
                        return False
                    # Check for collisions with other tetrominoes
                    if new_y >= 0 and grid_state[new_y][new_x] != 0:  # Assuming grid_state is a 2D list
                        logging.warning("Collision with another tetromino detected.")
                        return False
        return True
