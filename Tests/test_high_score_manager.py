import unittest
import json
import os
from high_score_manager import HighScoreManager

class TestHighScoreManager(unittest.TestCase):
    def setUp(self):
        """Setup before each test."""
        self.filename = 'all_time_high_scores.json'
        self.manager = HighScoreManager(self.filename)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_high_scores(self):
        """Test loading high scores from a valid file."""
        test_data = [[300, "2024-08-14 15:51:28"], [100, "2024-08-14 15:47:39"]]
        with open(self.filename, 'w') as f:
            json.dump(test_data, f)

        self.manager.load_high_scores()
        self.assertEqual(self.manager.high_scores, [(300, "2024-08-14 15:51:28"), (100, "2024-08-14 15:47:39")])

    def test_save_high_scores(self):
        """Test saving high scores to a file."""
        self.manager.add_high_score(500)
        self.manager.save_high_scores()

        with open(self.filename, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, [[500, "Invalid Timestamp"]])  # Check for the placeholder timestamp

    def test_handle_invalid_entry(self):
        """Test handling of invalid high score entries."""
        self.manager.high_scores = [(300, "2024-08-14 15:51:28"), "Invalid Entry"]
        self.manager.save_high_scores()

        with open(self.filename, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, [[300, "2024-08-14 15:51:28"], [0, "Invalid Timestamp"]])  # Check for handling

if __name__ == "__main__":
    unittest.main()