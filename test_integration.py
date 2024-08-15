import sys
import os

# Add the directory containing grid.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, Mock
import pygame
from tetris_game import TetrisGame

class TestTetrisGameIntegration(unittest.TestCase):
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('tetris_game.Tetromino')
    @patch('tetris_game.Grid')
    def test_game_initialization(self, MockGrid, MockTetromino, MockClock, mock_set_caption, mock_set_mode):
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Assertions
        mock_set_mode.assert_called_once_with((game.screen_width, game.screen_height))
        mock_set_caption.assert_called_once_with("Tetris")
        MockGrid.assert_called_once_with(width, height, block_size)
        MockTetromino.assert_called_once()
        self.assertEqual(game.score, 0)
        self.assertFalse(game.game_over)
        self.assertIsNotNone(game.clock)
        self.assertIsNotNone(game.current_tetromino)

    @patch('pygame.event.get')
    @patch('tetris_game.Grid')
    @patch('tetris_game.Tetromino')
    def test_tetromino_movement_and_placement(self, MockTetromino, MockGrid, mock_pygame_event_get):
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Set up the initial tetromino and grid state
        mock_tetromino_instance = MockTetromino.return_value
        mock_tetromino_instance.current_shape = [
            [1, 1],
            [1, 1]
        ]
        mock_grid_instance = MockGrid.return_value
        mock_grid_instance.is_valid_position.return_value = True
        mock_grid_instance.place_tetromino.return_value = 0  # No rows cleared

        # Set a fixed value for grid width to avoid mock chaining issues
        mock_grid_instance.width = 10  # Use a specific value instead of a mock return

        # Set the initial tetromino position to simulate the correct position after moving down
        game.tetromino_position = [0, mock_grid_instance.width // 2 - 1]

        # Simulate moving the tetromino down
        game.move_tetromino(0, 1)
        mock_grid_instance.is_valid_position.assert_called_once_with(mock_tetromino_instance, [1, game.tetromino_position[1]])

        # Simulate placing the tetromino
        game.place_current_tetromino()
        mock_grid_instance.place_tetromino.assert_called_once_with(mock_tetromino_instance, [1, game.tetromino_position[1]], True)  # Ensure True is included

    @patch('tetris_game.Grid')
    @patch('tetris_game.Tetromino')
    def test_row_clearing_and_score_update(self, MockTetromino, MockGrid):
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Set up the grid to simulate clearing rows
        mock_grid_instance = MockGrid.return_value
        mock_grid_instance.place_tetromino.return_value = 2  # Simulate 2 rows cleared

        # Place the tetromino and trigger row clearing
        game.place_current_tetromino()

        # Check that the score was updated correctly
        self.assertEqual(game.score, 200)

    @patch('tetris_game.Grid')
    @patch('tetris_game.Tetromino')
    def test_game_over(self, MockTetromino, MockGrid):
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Set up the grid to simulate a game over condition
        mock_grid_instance = MockGrid.return_value
        mock_grid_instance.is_valid_position.return_value = False

        # Manually trigger the check_game_over to simulate game over
        game.game_over = game.check_game_over()

        # Check that the game over condition is set
        self.assertTrue(game.game_over)

    @patch('tetris_game.Tetromino')
    @patch('tetris_game.Grid')
    @patch('pygame.time.get_ticks', return_value=1000)  # Mock get_ticks to return a consistent time
    def test_restart_game(self, mock_get_ticks, MockGrid, MockTetromino):
        # Initialize the game
        width, height, block_size = 10, 20, 30
        game = TetrisGame(width, height, block_size)

        # Simulate a game over scenario
        game.game_over = True

        # Call restart_game to reset the game state
        game.restart_game()

        # Assertions
        self.assertFalse(game.game_over)  # This should be False after restarting
        self.assertEqual(game.score, 0)
        self.assertEqual(game.tetromino_position, [0, game.grid.width // 2 - 1])
        self.assertEqual(game.last_drop_time, 1.0)

if __name__ == '__main__':
    unittest.main()