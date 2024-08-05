import pygame
import sys
from tetromino import Tetromino
from grid import Grid

class TetrisGame:
    def __init__(self, width=10, height=20, block_size=30):
        pygame.init()

        self.screen_width = width * block_size + 200  # Add 200 pixels for the score display
        self.screen_height = height * block_size
        self.fps = 60

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris")

        self.grid = Grid(width, height, block_size)

        self.clock = pygame.time.Clock()

        self.current_tetromino = Tetromino()
        self.tetromino_position = [0, width // 2 - 1]  # Start at the top of the grid

        self.score = 0  # Initialize the score at the start of the game

        self.drop_time = 0.75  # Time interval for dropping tetromino (750ms)
        self.last_drop_time = pygame.time.get_ticks() / 1000.0  # Track the last drop time in seconds

        print("Tetris game initialized. Falling delay set to 750ms.")

    def draw_game_over(self):
        font = pygame.font.Font(None, 74)  # Use a larger font for the game over message
        game_over_surface = font.render('Game Over', True, (255, 0, 0))  # Red color
        score_surface = font.render(f'Final Score: {self.score}', True, (255, 255, 255))  # White color for final score

        # Draw a black rectangle behind the text
        rect_width = max(game_over_surface.get_width(), score_surface.get_width()) + 20
        rect_height = game_over_surface.get_height() + score_surface.get_height() + 40  # Add space for score
        rect_x = self.screen_width // 2 - rect_width // 2
        rect_y = self.screen_height // 2 - rect_height // 2

        pygame.draw.rect(self.screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))  # Black rectangle
        pygame.draw.rect(self.screen, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height), 5)  # Red border

        self.screen.blit(game_over_surface, (self.screen_width // 2 - game_over_surface.get_width() // 2,
                                              self.screen_height // 2 - game_over_surface.get_height() // 2 - 20))
        self.screen.blit(score_surface, (self.screen_width // 2 - score_surface.get_width() // 2,
                                          self.screen_height // 2 + 20))  # Position the score below the game over message
        pygame.display.flip()  # Update the display to show the game over message
        pygame.time.wait(3000)  # Wait for 3 seconds before closing the game

    def run(self):
        running = True
        while running:
            try:
                current_time = pygame.time.get_ticks() / 1000.0  # Get the current time in seconds
                if current_time - self.last_drop_time >= self.drop_time:
                    print("Tetromino is about to drop.")
                    self.move_tetromino(0, 1)  # Move tetromino down
                    self.last_drop_time = current_time  # Reset the last drop time

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

                self.screen.fill((0, 0, 0))  # Fill with black background

                self.grid.draw(self.screen)

                self.draw_tetromino()

                self.draw_score()  # Add this line to draw the score

                # Check for game over condition after placing the tetromino
                if self.check_game_over():
                    self.draw_game_over()  # Call the new method to display "Game Over"
                    running = False  # End the game loop

                pygame.display.flip()
                self.clock.tick(self.fps)

            except Exception as e:
                print(f"An error occurred: {e}")

        pygame.quit()
        print("Tetris game exited.")

    def draw_score(self):
        font = pygame.font.Font(None, 36)  # Use default font and size 36
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))  # White color
        self.screen.blit(score_surface, (self.grid.width * self.grid.block_size + 20, 20))  # Position to the right of the grid

    def draw_tetromino(self):
        if self.current_tetromino:  # Check if current tetromino is valid
            shape = self.current_tetromino.current_shape  # Use the current shape matrix
            color = self.current_tetromino.get_color()

            print(f"Drawing Tetromino: shape: {shape}, color: {color}")

            for y, row in enumerate(shape):
                for x, block in enumerate(row):
                    if block:  # If the block is part of the tetromino
                        rect = pygame.Rect((self.tetromino_position[1] + x) * 30,
                                           (self.tetromino_position[0] + y) * 30,
                                           30, 30)
                        pygame.draw.rect(self.screen, color, rect)

    def move_tetromino(self, dx, dy):
        new_position = [self.tetromino_position[0] + dy, self.tetromino_position[1] + dx]
        print(f"Attempting to move tetromino to {new_position}")

        if self.grid.is_valid_position(self.current_tetromino, new_position):
            self.tetromino_position = new_position
            print(f"Moved tetromino to position: {self.tetromino_position}")
        else:
            if dy == 1:  # If moving down and collision occurs, place the tetromino
                print("Tetromino cannot move down further, placing tetromino")
                self.place_current_tetromino()

    def check_game_over(self):
        """Check if the game is over (i.e., if a new tetromino collides on spawn)."""
        if not self.grid.is_valid_position(self.current_tetromino, self.tetromino_position):
            print("Game Over: New tetromino cannot be placed.")
            return True
        return False

    def place_current_tetromino(self):
        try:
            filled_rows = self.grid.place_tetromino(self.current_tetromino, self.tetromino_position)
            print(f"place_current_tetromino: Filled rows: {filled_rows}")  # Debug print for filled rows
            if filled_rows > 0:
                self.update_score(filled_rows)
            else:
                print("No rows filled, update_score not called.")

            # Create a new tetromino
            self.current_tetromino = Tetromino()  # Create a new tetromino
            self.tetromino_position = [0, self.grid.width // 2 - 1]  # Reset position

            # Check for game over condition immediately after placing the tetromino
            if self.check_game_over():
                print("Game Over: New tetromino cannot be placed.")
                self.draw_game_over()  # Call the method to display "Game Over"
                pygame.quit()  # Close the game window
                sys.exit()  # Exit the program
        except (IndexError, ValueError) as e:  # Catch specific exceptions
            print(f"Error placing tetromino: {e}")  # Log the error message

    def update_score(self, filled_rows):
        print(f"update_score: Filled rows cleared: {filled_rows}")  # Debug print cleared rows
        self.score += filled_rows * 100  # Increment score by 100 for each row cleared
        print(f"update_score: Score updated: {self.score}")  # Debug print the updated score

    def rotate_tetromino(self):
        original_shape = self.current_tetromino.current_shape  # Backup the original shape

        if self.current_tetromino.rotate(self.grid.get_state(), self.tetromino_position):
            if not self.grid.is_valid_position(self.current_tetromino, self.tetromino_position):
                self.current_tetromino.current_shape = original_shape
                print(f"Collision detected, reverting rotation. Current position: {self.tetromino_position}, Original shape: {original_shape}")
            else:
                print("Tetromino rotated successfully.")
        else:
            print("Rotation failed, shape remains unchanged.")