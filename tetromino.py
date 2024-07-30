import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
        self.current_shape = self.get_shape()  # Store the current shape
        logging.debug(f"Tetromino created with shape: {self.shape} and color: {self.color}")

    def random_shape(self):
        shape = random.choice(list(self.shapes.keys()))
        logging.debug(f"DEBUG: Random shape selected: {shape}")
        return shape

    def get_shape(self):
        shape = self.shapes[self.shape]
        return shape

    def get_color(self):
        return self.color

    def rotate(self, grid_state):
        logging.debug(f"Rotating Tetromino: current shape type before rotation: {self.shape}")

        current_shape_matrix = self.get_shape()
        rotated_shape = [list(row) for row in zip(*current_shape_matrix[::-1])]
        logging.debug(f"Tetromino rotated to shape: {rotated_shape}")

        original_shape = self.get_shape()  # Get the original shape

        # Check for valid rotation
        if self.is_valid_rotation(rotated_shape, grid_state):
            self.shapes[self.shape] = rotated_shape  # Store the rotated shape
            self.current_shape = rotated_shape  # Update current shape
            logging.info("Tetromino rotated successfully.")
        else:
            logging.warning("Rotation invalid, reverting to original shape.")
            self.shapes[self.shape] = original_shape  # Revert to original shape
            self.current_shape = original_shape  # Restore current shape

    def is_valid_rotation(self, rotated_shape, grid_state):
        # Check for collisions with the grid boundaries and other tetrominoes
        for y, row in enumerate(rotated_shape):
            for x, block in enumerate(row):
                if block:  # If the block is part of the tetromino
                    # Check if the position is out of bounds
                    if x < 0 or x >= len(rotated_shape[0]) or y < 0 or y >= len(rotated_shape):
                        logging.warning("Collision with grid boundary detected.")
                        return False
                    # Check for collisions with other tetrominoes
                    if grid_state[y][x] != 0:  # Assuming grid_state is a 2D list
                        logging.warning("Collision with another tetromino detected.")
                        return False
        return True