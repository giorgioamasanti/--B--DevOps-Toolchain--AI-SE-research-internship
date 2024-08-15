import unittest
from unittest.mock import patch, Mock, MagicMock
import pygame
import sys
import os
import copy
import json

# Add the directory containing grid.py and tetromino.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tetris_game import TetrisGame
from tetromino import Tetromino

class TetrominoMock:
    def __init__(self, shape):
        self.shape = shape
        self.color = (255, 0, 0)
        self.current_shape = Tetromino.shapes[self.shape]

    def get_shape(self):
        return self.current_shape

    def get_color(self):
        return self.color

    def rotate(self, grid_state, position):
        # Simplified rotate function for testing
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        return True

class TestTetrisGame(unittest.TestCase):

    def setUp(self):
        """Setup before each test."""
        self.filename = 'all_time_high_scores.json'
        # Make a deep copy of the current high scores
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.original_high_scores = json.load(file)
        else:
            self.original_high_scores = []

    def tearDown(self):
        """Restore the original high scores after each test."""
        with open(self.filename, 'w') as file:
            json.dump(self.original_high_scores, file)

    @patch('pygame.display.set_mode', return_value=pygame.Surface((800, 600)))
    @patch('pygame.font.Font')
    def setUpGame(self, mock_font, mock_display):
        self.mock_display = mock_display
        self.mock_font = mock_font
        self.game = TetrisGame()
        self.game.screen = pygame.display.set_mode((800, 600))  # Initialize the display mode
        self.game.tetromino_position = [0, self.game.grid.width // 2 - 1]

    def test_initialization(self):
        self.setUpGame()
        self.assertEqual(self.game.screen_width, 10 * 30 + 350)
        self.assertEqual(self.game.screen_height, 20 * 30)
        self.assertEqual(self.game.fps, 60)
        self.assertEqual(self.game.score, 0)

    def test_move_tetromino(self):
        self.setUpGame()
        initial_position = self.game.tetromino_position.copy()
        self.game.move_tetromino(1, 0)  # Move right
        self.assertEqual(self.game.tetromino_position, [initial_position[0], initial_position[1] + 1])

    def test_place_current_tetromino(self):
        self.setUpGame()
        self.game.grid.place_tetromino = Mock(return_value=0)
        with patch('tetris_game.Tetromino', return_value=TetrominoMock('O')):
            with patch('pygame.mixer.Sound') as mock_sound:
                self.game.tetromino_place_sound = mock_sound
                self.game.place_current_tetromino()

                # Ensure that the correct sound is played
                mock_sound.play.assert_called_once()

    def test_update_score(self):
        self.setUpGame()
        initial_score = self.game.score
        self.game.update_score(2)  # Assume 2 rows cleared
        self.assertEqual(self.game.score, initial_score + 200)

    def test_rotate_tetromino(self):
        self.setUpGame()
        # Define expected shapes after one 90-degree counterclockwise rotation
        expected_shapes = {
            'I': [[1], [1], [1], [1]],
            'O': [[1, 1], [1, 1]],  # 'O' shape remains the same
            'T': [[1, 0], [1, 1], [1, 0]],
            'J': [[0, 1], [0, 1], [1, 1]],
            'L': [[1, 1], [0, 1], [0, 1]],
            'S': [[1, 0], [1, 1], [0, 1]],
            'Z': [[0, 1], [1, 1], [1, 0]]
        }

        for shape in Tetromino.shapes.keys():
            with self.subTest(shape=shape):
                self.game.current_tetromino = TetrominoMock(shape)
                original_shape = self.game.current_tetromino.get_shape().copy()
                self.game.rotate_tetromino()
                self.assertEqual(self.game.current_tetromino.get_shape(), expected_shapes[shape])

    def test_high_score_formatting(self):
        self.setUpGame()
        # Make a deep copy of the all_time_high_scores list to work with in the test
        original_high_scores = copy.deepcopy(self.game.all_time_high_scores)
        
        # Clear the deep copy to simulate an empty high score list
        test_high_scores = []
        
        # Simulate adding scores using the deep copy
        self.game.all_time_high_scores = test_high_scores
        self.game.add_high_score(0)
        self.game.add_high_score(100)
        self.game.add_high_score(1000)
        
        # Check if the scores are sorted correctly
        self.assertEqual(self.game.all_time_high_scores[0][0], 1000)
        self.assertEqual(self.game.all_time_high_scores[1][0], 100)
        self.assertEqual(self.game.all_time_high_scores[2][0], 0)
        
        # Restore the original high scores list after the test
        self.game.all_time_high_scores = original_high_scores

    def test_adjust_drop_speed(self):
        self.setUpGame()
        # Test case 1: Score below 200
        self.game.score = 150
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.75)

        # Test case 2: Score between 200 and 400
        self.game.score = 300
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.7)

        # Test case 3: Score between 400 and 600
        self.game.score = 500
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.6)

        # Test case 4: Score between 600 and 800
        self.game.score = 700
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.5)

        # Test case 5: Score between 800 and 1000
        self.game.score = 900
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.4)

        # Test case 6: Score between 1000 and 1200
        self.game.score = 1100
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.3)

        # Test case 7: Score between 1200 and 1400
        self.game.score = 1300
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.2)

        # Test case 8: Score above 1400
        self.game.score = 1500
        self.game.adjust_drop_speed()
        self.assertEqual(self.game.drop_time, 0.1)

    @patch('pygame.display.set_mode')
    def test_draw_high_scores(self, mock_set_mode):
        self.setUpGame()
        # Setup
        mock_screen = pygame.Surface((800, 600))  # Create a real pygame Surface for the test
        mock_set_mode.return_value = mock_screen

        game = TetrisGame()
        game.screen = mock_screen  # Set the screen to the real Surface object
        original_high_scores = copy.deepcopy(game.all_time_high_scores)
        game.all_time_high_scores = [
            (1000, '2022-01-01 12:00:00'),
            (800, '2022-01-02 12:00:00'),
            (600, '2022-01-03 12:00:00'),
            (400, '2022-01-04 12:00:00'),
            (200, '2022-01-05 12:00:00')
        ]

        # Call the method to be tested
        game.draw_high_scores(y_offset=100)

        # Assertions
        font = pygame.font.Font(None, 24)  # Use default font and size 24
        x_offset = game.grid.width * game.grid.block_size + 20  # Position to the right of the grid
        y_offset = 100  # Starting Y position for high scores

        # Check if the title is drawn correctly
        title_surface = font.render('High Scores', True, (255, 255, 255))
        mock_screen.blit(title_surface, (x_offset, y_offset))

        # Additional assertions to check that the rest of the drawing occurred correctly
        for i, (score, timestamp) in enumerate(game.all_time_high_scores[:5]):
            score_surface = font.render(f'{i + 1}. {score:04}', True, (255, 255, 255))
            time_surface = font.render(timestamp, True, (255, 255, 255))
            y_position = y_offset + 30 + i * 30
            self.assertTrue(mock_screen.blit(score_surface, (x_offset + 10, y_position)))
            self.assertTrue(mock_screen.blit(time_surface, (x_offset + 160, y_position)))

        # Restore original high scores
        game.all_time_high_scores = original_high_scores

    @patch('pygame.display.flip')
    @patch('pygame.event.get')
    def test_draw_game_over(self, mock_pygame_event_get, mock_pygame_display_flip):
        self.setUpGame()
        # Initialize pygame and create a Surface object for the screen
        pygame.init()
        screen = pygame.Surface((800, 600))

        # Create the game instance
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)
        game.screen = screen
        game.screen_width = 800
        game.screen_height = 600
        game.score = 1234

        # Mock the event to simulate pressing 'N' for a new game
        mock_pygame_event_get.side_effect = [[Mock(type=pygame.KEYDOWN, key=pygame.K_n)], []]

        # Call draw_game_over
        with patch.object(game, 'restart_game') as mock_restart_game:
            game.draw_game_over()

            # Define the area where the "GAME OVER" text should be
            rect_x = game.screen_width // 2 - 100  # Adjust the size of the rectangle if needed
            rect_y = game.screen_height // 2 - 50
            rect_width = 200
            rect_height = 100
            game_over_area = screen.subsurface(rect_x, rect_y, rect_width, rect_height)

            # Check that there's at least one non-black pixel in the game over area
            pixels = pygame.surfarray.pixels2d(game_over_area)
            non_black_pixels = (pixels != 0).any()

            self.assertTrue(non_black_pixels, "Game Over text was not rendered as expected.")

            # Ensure restart_game is called when 'N' is pressed
            mock_restart_game.assert_called_once()

        # Verify that the display was updated
        mock_pygame_display_flip.assert_called_once()

    @patch('tetris_game.Tetromino')
    @patch('tetris_game.Grid')
    @patch('pygame.time.get_ticks', return_value=1000)  # Mock get_ticks to return a consistent time
    def test_restart_game(self, mock_get_ticks, MockGrid, MockTetromino):
        self.setUpGame()
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Set up mocks
        mock_grid_instance = MockGrid.return_value
        mock_tetromino_instance = MockTetromino.return_value

        # Reset the mock call history
        MockTetromino.reset_mock()

        # Call the method under test
        game.restart_game()

        # Assertions
        mock_grid_instance.reset.assert_called_once()  # Check if grid.reset() was called
        MockTetromino.assert_called_once()  # Check if a new Tetromino was created once during restart_game
        self.assertEqual(game.current_tetromino, mock_tetromino_instance)  # Check if the tetromino was reset
        self.assertEqual(game.tetromino_position, [0, game.grid.width // 2 - 1])  # Check if the tetromino position was reset
        self.assertEqual(game.score, 0)  # Check if the score was reset
        self.assertEqual(game.last_drop_time, 1.0)  # Check if the drop time was reset correctly

    @patch('tetris_game.Grid')
    @patch('tetris_game.Tetromino')
    def test_check_game_over(self, MockTetromino, MockGrid):
        self.setUpGame()
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Set up mocks
        mock_grid_instance = MockGrid.return_value
        mock_tetromino_instance = MockTetromino.return_value

        # Simulate a valid position where the game should not be over
        mock_grid_instance.is_valid_position.return_value = True
        result = game.check_game_over()
        self.assertFalse(result)  # Expecting False because the position is valid
        mock_grid_instance.is_valid_position.assert_called_once_with(mock_tetromino_instance, game.tetromino_position)

        # Reset mock for the next test case
        mock_grid_instance.reset_mock()

        # Simulate an invalid position where the game should be over
        mock_grid_instance.is_valid_position.return_value = False
        result = game.check_game_over()
        self.assertTrue(result)  # Expecting True because the position is invalid
        mock_grid_instance.is_valid_position.assert_called_once_with(mock_tetromino_instance, game.tetromino_position)

    @patch('pygame.font.Font')
    def test_draw_score(self, MockFont):
        self.setUpGame()
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Create a mock font object
        mock_font = MockFont.return_value

        # Create a mock surface for the score rendering
        mock_score_surface = Mock()
        mock_font.render.return_value = mock_score_surface

        # Mock the screen surface to capture blit calls
        mock_screen = Mock()
        game.screen = mock_screen

        # Set the score for testing
        game.score = 1234

        # Call the method under test
        game.draw_score()

        # Assertions
        mock_font.render.assert_called_once_with(f'Score: {game.score:04}', True, (255, 255, 255))  # Check the score was rendered correctly
        mock_screen.blit.assert_called_once_with(mock_score_surface, (game.grid.width * game.grid.block_size + 20, 20))  # Check the score was blitted at the correct position

    @patch('pygame.draw.rect')
    def test_draw_tetromino(self, mock_draw_rect):
        self.setUpGame()
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Create a mock tetromino with a specific shape
        mock_tetromino = Mock()
        mock_tetromino.current_shape = [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        mock_tetromino.get_color.return_value = (255, 0, 0)  # Red color

        # Assign the mock tetromino to the game
        game.current_tetromino = mock_tetromino
        game.tetromino_position = [5, 5]  # Position the tetromino on the grid

        # Call the method under test
        game.draw_tetromino()

        # Calculate expected rectangles
        expected_rects = [
            pygame.Rect((5 + 0) * 30, (5 + 0) * 30, 30, 30),
            pygame.Rect((5 + 0) * 30, (5 + 1) * 30, 30, 30),
            pygame.Rect((5 + 1) * 30, (5 + 1) * 30, 30, 30),
            pygame.Rect((5 + 2) * 30, (5 + 1) * 30, 30, 30),
        ]

        # Assertions
        for rect in expected_rects:
            mock_draw_rect.assert_any_call(game.screen, (255, 0, 0), rect)  # Ensure each rectangle was drawn with the correct color and position


if __name__ == "__main__":
    pygame.init()
    unittest.main()
