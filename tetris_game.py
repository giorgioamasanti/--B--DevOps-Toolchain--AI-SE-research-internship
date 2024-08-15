import pygame
import sys
import os
from tetromino import Tetromino
from grid import Grid
from datetime import datetime  # Add this import at the beginning of the file
from high_score_manager import HighScoreManager  # Add this import at the top

class TetrisGame:
    def __init__(self, width=10, height=20, block_size=30):
        pygame.init()

        self.screen_width = width * block_size + 350
        self.screen_height = height * block_size
        self.fps = 60

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris")

        self.grid = Grid(width, height, block_size)

        self.clock = pygame.time.Clock()

        self.current_tetromino = Tetromino()
        self.tetromino_position = [0, width // 2 - 1]

        self.score = 0

        self.drop_time = 0.75
        self.last_drop_time = pygame.time.get_ticks() / 1000.0

        self.game_over = False

        self.high_score_manager = HighScoreManager()
        self.all_time_high_scores = self.high_score_manager.load_high_scores()  # Load all-time high scores
        if self.all_time_high_scores is None:
            self.all_time_high_scores = []

        self.current_session_scores = []  # Initialize an empty list for current session scores

        self.level_up_message = False
        self.level_up_timer = 0

        self.sound_effects_enabled = True

        pygame.mixer.init()
        self.tetromino_place_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/solidify.mp3'))
        self.row_clear_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/row_clear.mp3'))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/game_over.mp3'))
        print("Tetromino placement sound, row clear sound, and game over sound loaded successfully.")

        self.play_background_music()

        self.music_enabled = True
        print("Tetris game initialized. Falling delay set to 750ms.")

    def load_high_scores(self):
        """Load high scores from the HighScoreManager."""
        try:
            self.all_time_high_scores = self.high_score_manager.high_scores  # Load high scores
            print(f"High scores loaded: {self.all_time_high_scores}")  # Log loaded high scores
        except Exception as e:
            print(f"Error loading high scores: {e}")  # Log error with loading high scores

    def play_background_music(self):
        """Play background music continuously."""
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/background_music.mp3'))
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    def toggle_music(self):
        """Toggle the background music on and off."""
        if self.music_enabled:
            pygame.mixer.music.pause()  # Pause the music
            print("Music paused.")
        else:
            pygame.mixer.music.unpause()  # Unpause the music
            print("Music resumed.")
        self.music_enabled = not self.music_enabled  # Toggle the state

    def toggle_sound_effects(self):
        """Toggle the sound effects on and off."""
        self.sound_effects_enabled = not self.sound_effects_enabled  # Toggle the state
        if self.sound_effects_enabled:
            print("Sound effects enabled.")
        else:
            print("Sound effects disabled.")

    def add_high_score(self, score):
        """Add a new high score with the current timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(score, tuple):
            score = score[0]  # Extract the score if it's a tuple

        # Add to current session high scores
        self.current_session_scores.append((score, timestamp))
        self.current_session_scores.sort(key=lambda x: x[0], reverse=True)
        self.current_session_scores = self.current_session_scores[:5]

        # Update all-time high scores
        self.all_time_high_scores.append((score, timestamp))
        self.all_time_high_scores.sort(key=lambda x: x[0], reverse=True)
        self.all_time_high_scores = self.all_time_high_scores[:5]

        # Save the updated all-time high scores
        self.high_score_manager.save_high_scores(self.all_time_high_scores)
        print(f"Current session scores updated: {self.current_session_scores}")
        print(f"All-time high scores updated: {self.all_time_high_scores}")


    def adjust_drop_speed(self):
        """Adjust the drop speed based on the score."""
        print(f"Current score: {self.score}, Type: {type(self.score)}")  # Debugging output

        if isinstance(self.score, tuple):
            self.score = self.score[0]  # Fix the score if it's a tuple
        if self.score >= 1400:
            new_drop_time = 0.1
        elif self.score >= 1200:
            new_drop_time = 0.2
        elif self.score >= 1000:
            new_drop_time = 0.3
        elif self.score >= 800:
            new_drop_time = 0.4
        elif self.score >= 600:
            new_drop_time = 0.5
        elif self.score >= 400:
            new_drop_time = 0.6
        elif self.score >= 200:
            new_drop_time = 0.7
        else:
            new_drop_time = 0.75

        # Check if the drop time has changed
        if new_drop_time != self.drop_time:
            self.drop_time = new_drop_time
            self.level_up_message = True  # Set flag to show level up message
            self.level_up_timer = pygame.time.get_ticks() / 1000.0  # Reset the timer in seconds
            print(f"Drop speed adjusted to: {self.drop_time} seconds, Level Up Message triggered.")  # Log the adjustment

    def draw_high_score_table(self, y_offset):
        font = pygame.font.Font(None, 24)
        x_offset = self.grid.width * self.grid.block_size + 20

        # Title for the high score table
        title_surface = font.render('Current Session', True, (255, 255, 255))
        self.screen.blit(title_surface, (x_offset, y_offset))

        y_offset += 30  # Move Y position down for the header

        # Draw the header background with increased width
        header_background_rect = pygame.Rect(x_offset, y_offset, 320, 30)  # Increased width
        pygame.draw.rect(self.screen, (128, 128, 128), header_background_rect)  # Grey background

        # Draw the header text ("Score" and "Time") with adjusted position
        header_surface = font.render('Score                           Time', True, (0, 0, 0))  # Black text
        self.screen.blit(header_surface, (x_offset + 10, y_offset + 5))  # Adjust for padding

        y_offset += 30  # Move Y position down for the actual scores

        # Draw each high score entry
        for index, (score, timestamp) in enumerate(self.current_session_scores[:5]):  # Limit to top 5 scores
            score_surface = font.render(f'{score:04}', True, (255, 255, 255))  # White text for score
            time_surface = font.render(timestamp, True, (255, 255, 255))  # White text for timestamp
            self.screen.blit(score_surface, (x_offset + 10, y_offset + 5 + index * 30))  # Move text downwards slightly
            self.screen.blit(time_surface, (x_offset + 160, y_offset + 5 + index * 30))  # Move text downwards and to the right

        # Draw grid lines around the current session table
        table_width = 320  # Adjusted width of the table to match the header
        table_height = 150  # Adjusted height of the table
        grid_color = (128, 128, 128)  # Grey color for gridlines

        # Draw vertical lines
        pygame.draw.line(self.screen, grid_color, (x_offset, y_offset - 30), (x_offset, y_offset + table_height), 1)  # Left border
        pygame.draw.line(self.screen, grid_color, (x_offset + table_width, y_offset - 30), (x_offset + table_width, y_offset + table_height), 1)  # Right border
        pygame.draw.line(self.screen, grid_color, (x_offset + 150, y_offset - 30), (x_offset + 150, y_offset + table_height), 1)  # Vertical line slightly to the left

        # Draw horizontal lines
        pygame.draw.line(self.screen, grid_color, (x_offset, y_offset - 30), (x_offset + table_width, y_offset - 30), 1)  # Top border
        pygame.draw.line(self.screen, grid_color, (x_offset, y_offset + table_height), (x_offset + table_width, y_offset + table_height), 1)  # Bottom border
        for i in range(1, 6):  # Draw horizontal lines for each row in the table
            pygame.draw.line(self.screen, grid_color, (x_offset, y_offset + i * 30), (x_offset + table_width, y_offset + i * 30), 1)


    def draw_high_scores(self, y_offset):
        font = pygame.font.Font(None, 24)  # Use default font and size 24
        x_offset = self.grid.width * self.grid.block_size + 20  # Position to the right of the grid

        # Draw the title for high scores
        title_surface = font.render('High Scores', True, (255, 255, 255))  # White color
        self.screen.blit(title_surface, (x_offset, y_offset))

        y_offset += 30  # Move Y position down for the header

        # Draw the header background with increased width
        header_background_rect = pygame.Rect(x_offset, y_offset, 320, 30)  # Increased width
        pygame.draw.rect(self.screen, (128, 128, 128), header_background_rect)  # Grey background

        # Draw the header text ("Score" and "Time") with adjusted position
        header_surface = font.render('Score                           Time', True, (0, 0, 0))  # Black text
        self.screen.blit(header_surface, (x_offset + 10, y_offset + 5))  # Adjust for padding

        y_offset += 30  # Move Y position down for the actual scores

        # Draw each high score entry
        for index, (score, timestamp) in enumerate(self.all_time_high_scores[:5]):  # Limit to top 5 scores
            score_surface = font.render(f'{index + 1}. {score:04}', True, (255, 255, 255))  # White text for score
            time_surface = font.render(timestamp, True, (255, 255, 255))  # White text for timestamp
            self.screen.blit(score_surface, (x_offset + 10, y_offset + 5 + index * 30))  # Move text downwards slightly
            self.screen.blit(time_surface, (x_offset + 160, y_offset + 5 + index * 30))  # Move text downwards and to the right

        # Draw grid lines around the all-time high score table
        table_width = 320  # Adjusted width of the table to match the header
        table_height = 150  # Adjusted height of the table
        grid_color = (128, 128, 128)  # Grey color for gridlines

        # Draw vertical lines
        pygame.draw.line(self.screen, grid_color, (x_offset, y_offset - 30), (x_offset, y_offset + table_height), 1)  # Left border
        pygame.draw.line(self.screen, grid_color, (x_offset + table_width, y_offset - 30), (x_offset + table_width, y_offset + table_height), 1)  # Right border
        pygame.draw.line(self.screen, grid_color, (x_offset + 150, y_offset - 30), (x_offset + 150, y_offset + table_height), 1)  # Vertical line slightly to the left

        # Draw horizontal lines
        pygame.draw.line(self.screen, grid_color, (x_offset, y_offset - 30), (x_offset + table_width, y_offset - 30), 1)  # Top border
        pygame.draw.line(self.screen, grid_color, (x_offset, y_offset + table_height), (x_offset + table_width, y_offset + table_height), 1)  # Bottom border
        for i in range(1, 6):  # Draw horizontal lines for each row in the table
            pygame.draw.line(self.screen, grid_color, (x_offset, y_offset + i * 30), (x_offset + table_width, y_offset + i * 30), 1)


    def draw_game_over(self):
        font = pygame.font.Font(None, 20)  # Adjusted font size for the game over message
        game_over_surface = font.render('GAME OVER', True, (255, 0, 0))  # Red color
        score_surface = font.render(f'Score: {self.score:04}', True, (255, 255, 255))  # Format final score to 4 digits
        prompt_surface = font.render("Press 'N' for a new game", True, (255, 255, 255))  # New prompt for starting a new game

        # Adjust the rectangle width and height to ensure it fits all text neatly
        text_height = max(game_over_surface.get_height(), score_surface.get_height(), prompt_surface.get_height())
        rect_height = text_height * 3 + 40  # Add padding between the text lines and around the edges
        rect_width = max(game_over_surface.get_width(), score_surface.get_width(), prompt_surface.get_width()) + 80  # Increased padding

        print(f"Game Over Screen Dimensions - Width: {rect_width}, Height: {rect_height}")

        rect_x = self.screen_width // 2 - rect_width // 2
        rect_y = self.screen_height // 2 - rect_height // 2

        pygame.draw.rect(self.screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))  # Black rectangle
        pygame.draw.rect(self.screen, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height), 5)  # Red border

        self.screen.blit(game_over_surface, (self.screen_width // 2 - game_over_surface.get_width() // 2,
                                              self.screen_height // 2 - rect_height // 2 + 10))
        self.screen.blit(score_surface, (self.screen_width // 2 - score_surface.get_width() // 2,
                                          self.screen_height // 2 - rect_height // 2 + 30))  # Position the score below the game over message
        self.screen.blit(prompt_surface, (self.screen_width // 2 - prompt_surface.get_width() // 2,
                                           self.screen_height // 2 - rect_height // 2 + 50))  # Position the prompt below the score
        pygame.display.flip()  # Update the display to show the game over message

        print(f"Drawing Game Over Rectangle at X: {rect_x}, Y: {rect_y}")

        # Log the dimensions of each text surface
        print(f"Game Over Text Surface Dimensions - Game Over: {game_over_surface.get_width()}x{game_over_surface.get_height()}")
        print(f"Score Text Surface Dimensions - Score: {score_surface.get_width()}x{score_surface.get_height()}")
        print(f"Prompt Text Surface Dimensions - Prompt: {prompt_surface.get_width()}x{prompt_surface.get_height()}")

        # Log the calculated rectangle dimensions before drawing
        print(f"Final Game Over Rectangle Dimensions - Width: {rect_width}, Height: {rect_height}")

        # Allow for immediate input handling
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # Check for 'N' key press
                        self.restart_game()  # Restart the game
                        self.game_over = False  # Reset game over flag
                        waiting = False  # Exit the waiting loop
                    elif event.key == pygame.K_ESCAPE:  # Allow quitting the game
                        pygame.quit()
                        sys.exit()
        print("Game restarted from game over screen.")  # Log for debugging

    def restart_game(self):
        """Reset the game state for a new game."""
        self.grid.reset()  # Reset the grid
        self.current_tetromino = Tetromino()  # Create a new tetromino
        self.tetromino_position = [0, self.grid.width // 2 - 1]  # Reset tetromino position
        self.score = 0  # Reset the score
        self.last_drop_time = pygame.time.get_ticks() / 1000.0  # Reset drop time to current time
        self.game_over = False  # Ensure game_over is reset
        self.level_up_message = False  # Reset level up message flag
        print("Game restarted.")

    def run(self):
        running = True
        while running:
            try:
                if self.game_over:  # If game is over, skip the game logic
                    continue

                current_time = pygame.time.get_ticks() / 1000.0  # Get the current time in seconds
                if current_time - self.last_drop_time >= self.drop_time:
                    print("Tetromino is about to drop.")
                    self.move_tetromino(0, 1)  # Move tetromino down
                    self.last_drop_time = current_time  # Reset the last drop time

                self.adjust_drop_speed()  # Call to adjust drop speed based on score

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
                        elif event.key == pygame.K_m:  # Check for 'M' key press
                            self.toggle_music()  # Toggle music
                        elif event.key == pygame.K_s:  # Check for 'S' key press
                            self.toggle_sound_effects()  # Toggle sound effects

                self.screen.fill((0, 0, 0))  # Fill with black background

                self.grid.draw(self.screen)

                self.draw_tetromino()

                self.draw_score()  # Draw the current score
                current_session_offset = 60  # Adjust as necessary to create space between sections
                self.draw_high_score_table(current_session_offset)

                all_time_high_scores_offset = current_session_offset + 240  # Adjust as necessary based on the height of the session table
                self.draw_high_scores(all_time_high_scores_offset)

                # Check for game over condition after placing the tetromino
                if self.check_game_over():
                    self.game_over = True  # Set game over flag
                    self.add_high_score(self.score)  # Add the current score to high scores
                    if self.sound_effects_enabled:  # Check if sound effects are enabled before playing sound
                        self.grid.play_game_over_sound()  # Play sound effect for game over
                    self.draw_game_over()  # Call to display "Game Over"
                    continue  # Skip to next iteration to wait for user input

                if self.level_up_message:
                    if (current_time - self.level_up_timer) < 2:  # Display for 2 seconds
                        # Create a white box behind the level up text
                        level_up_surface = pygame.font.Font(None, 48).render('Level Up!', True, (0, 0, 0))  # Black text
                        box_width = level_up_surface.get_width() + 20  # Add padding to the box width
                        box_height = level_up_surface.get_height() + 10  # Add padding to the box height
                        box_x = self.screen_width // 2 - box_width // 2  # Center the box horizontally
                        box_y = self.screen_height // 2 - box_height // 2  # Center the box vertically

                        # Draw the white box
                        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height))  # White box
                        self.screen.blit(level_up_surface, (self.screen_width // 2 - level_up_surface.get_width() // 2, self.screen_height // 2 - level_up_surface.get_height() // 2))  # Draw text
                        print("Level Up message displayed with background box.")  # Log when the message is displayed
                    else:
                        self.level_up_message = False  # Reset the level up message flag after display time
                        print("Level Up message cleared.")  # Log when the message is cleared

                pygame.display.flip()
                self.clock.tick(self.fps)

            except Exception as e:
                print(f"An error occurred: {e}")

        pygame.quit()
        print("Tetris game exited.")

    def draw_score(self):
        font = pygame.font.Font(None, 36)  # Use default font and size 36
        score = self.score if isinstance(self.score, int) else self.score[0]
        score_surface = font.render(f'Score: {score:04}', True, (255, 255, 255))  # Ensure score is an integer
        self.screen.blit(score_surface, (self.grid.width * self.grid.block_size + 20, 20))  # Position to the right of the grid

    def draw_tetromino(self):
        if self.current_tetromino:  # Check if current tetromino is valid
            shape = self.current_tetromino.current_shape  # Use the current shape matrix
            color = self.current_tetromino.get_color()

            #print(f"Drawing Tetromino: shape: {shape}, color: {color}")

            for y, row in enumerate(shape):
                for x, block in enumerate(row):
                    if block:  # If the block is part of the tetromino
                        rect = pygame.Rect((self.tetromino_position[1] + x) * 30,
                                           (self.tetromino_position[0] + y) * 30,
                                           30, 30)
                        pygame.draw.rect(self.screen, color, rect)

    def move_tetromino(self, dx, dy):
        new_position = [self.tetromino_position[0] + dy, self.tetromino_position[1] + dx]
        #print(f"Attempting to move tetromino to {new_position}")

        if self.grid.is_valid_position(self.current_tetromino, new_position):
            self.tetromino_position = new_position
            #print(f"Moved tetromino to position: {self.tetromino_position}")
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
            filled_rows = self.grid.place_tetromino(self.current_tetromino, self.tetromino_position, self.sound_effects_enabled)
            print(f"place_current_tetromino: Filled rows: {filled_rows}")  # Debug print for filled rows
            if filled_rows > 0:
                self.update_score(filled_rows)
                if self.sound_effects_enabled:  # Check if sound effects are enabled before playing sound
                    self.grid.row_clear_sound.play()  # Play sound effect when rows are cleared
            else:
                print("No rows filled, update_score not called.")

            # Play the sound effect when a tetromino is placed
            if self.sound_effects_enabled:  # Check if sound effects are enabled before playing sound
                self.tetromino_place_sound.play()  # Play the sound effect when a tetromino is placed

            # Create a new tetromino
            self.current_tetromino = Tetromino()  # Create a new tetromino
            self.tetromino_position = [0, self.grid.width // 2 - 1]  # Reset position

            # Check for game over condition immediately after placing the tetromino
            if self.check_game_over():
                print("Game Over: New tetromino cannot be placed.")
                self.add_high_score(self.score)  # Add the current score to high scores
                if self.sound_effects_enabled:  # Check if sound effects are enabled before playing sound
                    self.grid.play_game_over_sound()  # Play sound effect for game over
                self.draw_game_over()  # Call the method to display "Game Over"
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
        print(f'High Scores List: {self.all_time_high_scores}')  # Log high scores for debugging
        for index, entry in enumerate(self.all_time_high_scores[:5]):  # Log top 5 high scores
            print(f'Entry at index {index}: {entry}, Type: {type(entry)}')  # Log entry and its type
            if isinstance(entry, tuple) and len(entry) == 2:
                score, timestamp = entry
                print(f'Rendering Score: {score}, Timestamp: {timestamp}')  # Log score and timestamp before rendering
            else:
                print(f'Unexpected entry format at index {index}: {entry}')  # Log unexpected format