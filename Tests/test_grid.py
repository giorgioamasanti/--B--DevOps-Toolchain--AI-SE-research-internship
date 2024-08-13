import unittest
import pygame
import sys
import os

# Add the directory containing grid.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grid import Grid
import pygame

class TetrominoMock:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def get_shape(self):
        return self.shape

    def get_color(self):
        return self.color

    def rotate(self, grid_state):
        # Simplified rotate function for testing
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        return True

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()
        self.grid.tetromino_position = (0, 0)  # Define tetromino_position for testing rotate_tetromino

    def test_initialization(self):
        self.assertEqual(self.grid.width, 10)
        self.assertEqual(self.grid.height, 20)
        self.assertEqual(len(self.grid.grid), 20)
        self.assertEqual(len(self.grid.grid[0]), 10)

    def test_reset(self):
        self.grid.grid[0][0] = 1
        self.grid.reset()
        self.assertEqual(self.grid.grid, [[0 for _ in range(10)] for _ in range(20)])

    def test_is_full(self):
        self.assertFalse(self.grid.is_full())
        self.grid.grid[0][0] = 1
        self.assertTrue(self.grid.is_full())

    def test_place_tetromino(self):
        tetromino = TetrominoMock([[1, 1], [1, 1]], (255, 0, 0))
        cleared_rows = self.grid.place_tetromino(tetromino, (0, 0))
        self.assertEqual(cleared_rows, 0)
        self.assertEqual(self.grid.grid[0][0], 1)
        self.assertEqual(self.grid.color_grid[0][0], (255, 0, 0))

    def test_place_tetromino_out_of_bounds(self):
        tetromino = TetrominoMock([[1, 1], [1, 1]], (255, 0, 0))
        cleared_rows = self.grid.place_tetromino(tetromino, (-1, -1))
        self.assertEqual(cleared_rows, 0)

    def test_check_filled_rows(self):
        self.grid.grid[19] = [1 for _ in range(10)]
        filled_rows = self.grid.check_filled_rows()
        self.assertEqual(filled_rows, [19])

    def test_clear_filled_rows(self):
        self.grid.grid[19] = [1 for _ in range(10)]
        cleared_rows = self.grid.clear_filled_rows()
        self.assertEqual(cleared_rows, 1)
        self.assertEqual(self.grid.grid[19], [0 for _ in range(10)])

    def test_rotate_tetromino(self):
        tetromino = TetrominoMock([[1, 1, 1], [0, 1, 0]], (0, 255, 0))
        self.assertTrue(self.grid.rotate_tetromino(tetromino))
        self.assertEqual(tetromino.get_shape(), [[0, 1], [1, 1], [0, 1]])

    def test_draw(self):
        pygame.init()
        screen = pygame.display.set_mode((self.grid.width * self.grid.block_size, self.grid.height * self.grid.block_size))
        self.grid.draw(screen)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second to see the drawn grid
        pygame.quit()

    def test_is_valid_position(self):
        tetromino = TetrominoMock([[1, 1], [1, 1]], (255, 0, 0))
        self.grid.grid[0][0] = 1
        self.assertFalse(self.grid.is_valid_position(tetromino, (0, 0)))
        self.assertTrue(self.grid.is_valid_position(tetromino, (1, 1)))
        self.assertFalse(self.grid.is_valid_position(tetromino, (19, 9)))

    def test_get_state(self):
        expected_state = [[0 for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        self.assertEqual(self.grid.get_state(), expected_state)

if __name__ == "__main__":
    pygame.init()
    unittest.main()
