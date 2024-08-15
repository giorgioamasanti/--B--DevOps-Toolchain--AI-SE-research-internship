import unittest
import json
import copy
import sys
import os
import tempfile

# Add the directory containing grid.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from high_score_manager import HighScoreManager

class TestHighScoreManager(unittest.TestCase):
    def setUp(self):
        """Setup before each test."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()  # Close the file so it can be used by HighScoreManager

        # Initialize HighScoreManager with the temporary file
        self.manager = HighScoreManager(self.temp_file.name)

        # Make a deep copy of the original high scores
        self.original_high_scores = copy.deepcopy(self.manager.high_scores)

    def tearDown(self):
        """Clean up after each test."""
        # Restore the original high scores from the deep copy
        self.manager.high_scores = self.original_high_scores
        self.manager.save_high_scores()

        # Remove the temporary test file
        os.remove(self.temp_file.name)

    def test_load_high_scores(self):
        """Test loading high scores from a valid file."""
        # Prepare test data as list of lists (mimicking file format)
        test_data = [[300, "2024-08-14 15:51:28"], [100, "2024-08-14 15:47:39"]]
        with open(self.temp_file.name, 'w') as f:
            json.dump(test_data, f)

        # Load high scores, which should now validate the entries
        loaded_high_scores = self.manager.load_high_scores()
        
        # Convert the test data to tuples for comparison
        expected_high_scores = [(300, "2024-08-14 15:51:28"), (100, "2024-08-14 15:47:39")]
        
        self.assertEqual(loaded_high_scores, expected_high_scores)

    def test_save_high_scores(self):
        """Test saving high scores to a file."""
        self.manager.high_scores = copy.deepcopy(self.original_high_scores)  # Work with a deep copy
        self.manager.add_high_score(500)
        self.manager.save_high_scores()

        with open(self.temp_file.name, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 500)


if __name__ == "__main__":
    unittest.main()
