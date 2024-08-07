import unittest
from unittest.mock import patch, Mock
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

if __name__ == "__main__":
    pygame.init()
    unittest.main()
