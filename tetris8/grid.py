import pygame

class Grid:
    def __init__(self, width=10, height=20, block_size=30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.color_grid = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]  # New grid for colors

    def draw(self, surface):
        # Fill the background with black
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
                        raise ValueError("Tetromino position is out of bounds.")
        print(f"Tetromino placed at position: {position} with color: {color}")  # Log tetromino placement

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