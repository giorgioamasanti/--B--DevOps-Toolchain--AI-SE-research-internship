import sys
import os

# Add the directory containing grid.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
import copy
from high_score_manager import HighScoreManager

class TestHighScoreManager(unittest.TestCase):
    def setUp(self):
        """Setup before each test."""
        self.filename = 'all_time_high_scores.json'
        self.manager = HighScoreManager(self.filename)

        # Make a deep copy of the original high scores to restore after the test
        self.original_high_scores = copy.deepcopy(self.manager.high_scores)

    def tearDown(self):
        """Clean up after each test."""
        # Restore the original high scores from the deep copy
        self.manager.high_scores = self.original_high_scores
        self.manager.save_high_scores()

        # Remove the test file if it was created
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_high_scores(self):
        """Test loading high scores from a valid file."""
        # Prepare test data as list of lists (mimicking file format)
        test_data = [[300, "2024-08-14 15:51:28"], [100, "2024-08-14 15:47:39"]]
        with open(self.filename, 'w') as f:
            json.dump(test_data, f)

        # Load high scores, which converts the lists into tuples
        self.manager.load_high_scores()
        
        # Convert loaded data to list of tuples
        loaded_high_scores = [(score, timestamp) for score, timestamp in self.manager.high_scores]
        
        # Convert test data to list of tuples for the assertion
        expected_high_scores = [(300, "2024-08-14 15:51:28"), (100, "2024-08-14 15:47:39")]
        
        self.assertEqual(loaded_high_scores, expected_high_scores)

    def test_save_high_scores(self):
        """Test saving high scores to a file."""
        self.manager.high_scores = copy.deepcopy(self.original_high_scores)  # Work with a deep copy
        self.manager.add_high_score(500)
        self.manager.save_high_scores()

        with open(self.filename, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 500)

    def test_handle_invalid_entry(self):
        """Test handling of invalid high score entries."""
        self.manager.high_scores = [(300, "2024-08-14 15:51:28"), "Invalid Entry"]
        self.manager.save_high_scores()

        with open(self.filename, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, [[300, "2024-08-14 15:51:28"], [0, "Invalid Timestamp"]])  # Check for handling

if __name__ == "__main__":
    unittest.main()