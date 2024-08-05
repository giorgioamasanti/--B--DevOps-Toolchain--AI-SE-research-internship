import unittest
import sys
import os

# Add the directory containing tetromino.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tetromino import Tetromino

class TestTetromino(unittest.TestCase):
    def setUp(self):
        self.shapes = {
            'I': [[1, 1, 1, 1]],
            'O': [[1, 1],
                  [1, 1]],
            'T': [[0, 1, 0],
                  [1, 1, 1]],
            'J': [[1, 1, 1],
                  [0, 0, 1]],
            'L': [[1, 1, 1],
                  [1, 0, 0]],
            'S': [[0, 1, 1],
                  [1, 1, 0]],
            'Z': [[1, 1, 0],
                  [0, 1, 1]]
        }
        self.expected_rotations = {
            'I': [[1], [1], [1], [1]],
            'O': [[1, 1], [1, 1]],  # 'O' shape remains the same
            'T': [[1, 0], [1, 1], [1, 0]],
            'J': [[0, 1], [0, 1], [1, 1]],
            'L': [[1, 1], [0, 1], [0, 1]],
            'S': [[1, 0], [1, 1], [0, 1]],
            'Z': [[0, 1], [1, 1], [1, 0]]
        }

    def test_random_shape(self):
        tetromino = Tetromino()
        self.assertIn(tetromino.shape, self.shapes.keys())

    def test_get_shape(self):
        for shape, matrix in self.shapes.items():
            tetromino = Tetromino()
            tetromino.shape = shape
            tetromino.current_shape = matrix
            self.assertEqual(tetromino.get_shape(), matrix)

    def test_get_color(self):
        colors = {
            'I': (0, 255, 255),
            'O': (255, 255, 0),
            'T': (128, 0, 128),
            'J': (0, 0, 255),
            'L': (255, 165, 0),
            'S': (0, 255, 0),
            'Z': (255, 0, 0)
        }
        for shape, color in colors.items():
            tetromino = Tetromino()
            tetromino.shape = shape
            tetromino.color = color
            self.assertEqual(tetromino.get_color(), color)

    def test_rotate(self):
        grid_state = [[0]*10 for _ in range(20)]  # Empty grid for simplicity
        position = [0, 0]  # Position for simplicity

        for shape, expected in self.expected_rotations.items():
            tetromino = Tetromino()
            tetromino.shape = shape
            tetromino.current_shape = self.shapes[shape]
            tetromino.rotate(grid_state, position)
            self.assertEqual(tetromino.get_shape(), expected)

    def test_is_valid_rotation(self):
        tetromino = Tetromino()
        grid_state = [[0]*10 for _ in range(20)]
        position = [0, 0]

        for shape in self.shapes.keys():
            tetromino.shape = shape
            tetromino.current_shape = self.shapes[shape]
            rotated_shape = [list(row) for row in zip(*tetromino.current_shape[::-1])]
            self.assertTrue(tetromino.is_valid_rotation(rotated_shape, grid_state, position))

if __name__ == "__main__":
    unittest.main()
