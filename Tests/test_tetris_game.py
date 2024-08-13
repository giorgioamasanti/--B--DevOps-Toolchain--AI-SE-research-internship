import unittest
from unittest.mock import patch, Mock, call
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

    @patch('pygame.font.Font')
    @patch('pygame.display.set_mode')
    def test_draw_high_score_table(self, mock_set_mode, mock_font):
        # Setup
        mock_screen = pygame.Surface((650, 600))  # Create a real pygame.Surface with the actual dimensions
        mock_set_mode.return_value = mock_screen
        mock_font_instance = mock_font.return_value
        mock_font_instance.render.return_value = pygame.Surface((100, 30))  # Mock render return value

        game = TetrisGame()
        game.screen = mock_screen  # Set the screen to the real pygame.Surface
        game.high_scores = [
            (1000, '2022-01-01 12:00:00'),
            (800, '2022-01-02 12:00:00'),
            (600, '2022-01-03 12:00:00'),
            (400, '2022-01-04 12:00:00'),
            (200, '2022-01-05 12:00:00')
        ]

        # Call the method to be tested
        game.draw_high_score_table()

        # Assertions
        expected_calls = [
            call.render('Current Session', True, (255, 255, 255)),
            call.render('Score     Time', True, (0, 0, 0)),
            call.render('1000', True, (255, 255, 255)),
            call.render('2022-01-01 12:00:00', True, (255, 255, 255)),
            call.render('800', True, (255, 255, 255)),
            call.render('2022-01-02 12:00:00', True, (255, 255, 255)),
            call.render('600', True, (255, 255, 255)),
            call.render('2022-01-03 12:00:00', True, (255, 255, 255)),
            call.render('400', True, (255, 255, 255)),
            call.render('2022-01-04 12:00:00', True, (255, 255, 255)),
            call.render('200', True, (255, 255, 255)),
            call.render('2022-01-05 12:00:00', True, (255, 255, 255))
        ]
        mock_font.assert_called_once_with(None, 24)
        mock_set_mode.assert_called_once_with((650, 600))  # Update to match the actual dimensions
        mock_font_instance.render.assert_has_calls(expected_calls, any_order=True)
    
    @patch('pygame.font.Font')
    @patch('pygame.display.set_mode')
    def test_draw_high_score_table(self, mock_set_mode, mock_font):
        # Setup
        mock_screen = pygame.Surface((650, 600))  # Create a real pygame.Surface with the actual dimensions
        mock_set_mode.return_value = mock_screen
        mock_font_instance = mock_font.return_value
        mock_font_instance.render.return_value = pygame.Surface((100, 30))  # Mock render return value

        game = TetrisGame()
        game.screen = mock_screen  # Set the screen to the real pygame.Surface
        game.high_scores = [
            (1000, '2022-01-01 12:00:00'),
            (800, '2022-01-02 12:00:00'),
            (600, '2022-01-03 12:00:00'),
            (400, '2022-01-04 12:00:00'),
            (200, '2022-01-05 12:00:00')
        ]

        # Call the method to be tested
        game.draw_high_score_table()

        # Assertions
        expected_calls = [
            call.render('Current Session', True, (255, 255, 255)),
            call.render('Score     Time', True, (0, 0, 0)),
            call.render('1000', True, (255, 255, 255)),
            call.render('2022-01-01 12:00:00', True, (255, 255, 255)),
            call.render('0800', True, (255, 255, 255)),  # Update to match the actual values
            call.render('2022-01-02 12:00:00', True, (255, 255, 255)),
            call.render('0600', True, (255, 255, 255)),  # Update to match the actual values
            call.render('2022-01-03 12:00:00', True, (255, 255, 255)),
            call.render('0400', True, (255, 255, 255)),  # Update to match the actual values
            call.render('2022-01-04 12:00:00', True, (255, 255, 255)),
            call.render('0200', True, (255, 255, 255)),  # Update to match the actual values
            call.render('2022-01-05 12:00:00', True, (255, 255, 255))
        ]
        mock_font.assert_called_once_with(None, 24)
        mock_set_mode.assert_called_once_with((650, 600))  # Update to match the actual dimensions
        mock_font_instance.render.assert_has_calls(expected_calls, any_order=True)

if __name__ == "__main__":
    pygame.init()
    unittest.main()
