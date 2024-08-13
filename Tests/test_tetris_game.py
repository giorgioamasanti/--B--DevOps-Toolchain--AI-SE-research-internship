import unittest
from unittest.mock import patch, Mock, call, MagicMock
import pygame
import sys
import os

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
    @patch('pygame.display.set_mode', return_value=pygame.Surface((800, 600)))
    @patch('pygame.font.Font')
    def setUp(self, mock_font, mock_display):
        self.mock_display = mock_display
        self.mock_font = mock_font
        self.game = TetrisGame()
        self.game.screen = pygame.display.set_mode((800, 600))  # Initialize the display mode
        self.game.tetromino_position = [0, self.game.grid.width // 2 - 1]

    def test_initialization(self):
        self.assertEqual(self.game.screen_width, 10 * 30 + 350)
        self.assertEqual(self.game.screen_height, 20 * 30)
        self.assertEqual(self.game.fps, 60)
        self.assertEqual(self.game.score, 0)

    def test_move_tetromino(self):
        initial_position = self.game.tetromino_position.copy()
        self.game.move_tetromino(1, 0)  # Move right
        self.assertEqual(self.game.tetromino_position, [initial_position[0], initial_position[1] + 1])

    def test_place_current_tetromino(self):
        self.game.grid.place_tetromino = Mock(return_value=0)
        with patch('tetris_game.Tetromino', return_value=TetrominoMock('O')):  # Ensure new tetromino is a mock
            self.game.place_current_tetromino()
            self.assertIsInstance(self.game.current_tetromino, TetrominoMock)
            self.assertEqual(self.game.tetromino_position, [0, self.game.grid.width // 2 - 1])

    def test_update_score(self):
        initial_score = self.game.score
        self.game.update_score(2)  # Assume 2 rows cleared
        self.assertEqual(self.game.score, initial_score + 200)

    def test_rotate_tetromino(self):
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
        self.game.add_high_score(0)
        self.game.add_high_score(100)
        self.game.add_high_score(1000)
        self.assertEqual(self.game.high_scores[0][0], 1000)
        self.assertEqual(self.game.high_scores[1][0], 100)
        self.assertEqual(self.game.high_scores[2][0], 0)

    def test_add_high_score(self):
        initial_scores = self.game.high_scores.copy()
        self.game.add_high_score(500)
        self.assertEqual(len(self.game.high_scores), len(initial_scores) + 1)
        self.assertEqual(self.game.high_scores[0][0], 500)
        if initial_scores:
            self.assertGreaterEqual(self.game.high_scores[0][1], initial_scores[0][1])

    def test_adjust_drop_speed(self):
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
        # Setup
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen

        game = TetrisGame()
        game.screen = mock_screen  # Set the screen to the mock object
        game.high_scores = [
            (1000, '2022-01-01 12:00:00'),
            (800, '2022-01-02 12:00:00'),
            (600, '2022-01-03 12:00:00'),
            (400, '2022-01-04 12:00:00'),
            (200, '2022-01-05 12:00:00')
        ]

        # Call the method to be tested
        game.draw_high_scores()

        # Assertions
        font = pygame.font.Font(None, 24)  # Use default font and size 24
        x_offset = game.grid.width * game.grid.block_size + 20  # Position to the right of the grid
        y_offset = 100  # Starting Y position for high scores

        # Check if the title is drawn correctly
        title_surface = font.render('High Scores', True, (255, 255, 255))
        mock_screen.blit.assert_any_call(title_surface, (x_offset, y_offset))

    @patch('pygame.display.set_mode')
    def test_draw_high_scores(self, mock_set_mode):
        # Setup
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen

        game = TetrisGame()
        game.screen = mock_screen  # Set the screen to the mock object
        game.high_scores = [
            (1000, '2022-01-01 12:00:00'),
            (800, '2022-01-02 12:00:00'),
            (600, '2022-01-03 12:00:00'),
            (400, '2022-01-04 12:00:00'),
            (200, '2022-01-05 12:00:00')
        ]

        # Call the method to be tested
        game.draw_high_scores()

        # Assertions
        font = pygame.font.Font(None, 24)  # Use default font and size 24
        x_offset = game.grid.width * game.grid.block_size + 20  # Position to the right of the grid
        y_offset = 100  # Starting Y position for high scores

        # Check if the title is drawn correctly
        title_surface = font.render('High Scores', True, (255, 255, 255))
        expected_call = (title_surface, (x_offset, y_offset))
        print(f"Expected blit call: {expected_call}")
        print(f"Actual blit calls: {mock_screen.blit.call_args_list}")

        # Extract the actual calls
        actual_calls = mock_screen.blit.call_args_list

        # Check if the expected call is in the actual calls
        found = False
        for call in actual_calls:
            args, kwargs = call
            surface, position = args
            if position == (x_offset, y_offset) and surface.get_size() == title_surface.get_size() and surface.get_at((0, 0)) == title_surface.get_at((0, 0)):
                found = True
                break

        self.assertTrue(found, f"Expected blit call {expected_call} not found in actual calls {actual_calls}")

    @patch('pygame.display.flip')
    @patch('pygame.event.get')
    def test_draw_game_over(self, mock_pygame_event_get, mock_pygame_display_flip):
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


if __name__ == "__main__":
    pygame.init()
    unittest.main()
