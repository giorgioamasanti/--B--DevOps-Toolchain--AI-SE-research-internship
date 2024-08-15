import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HighScoreManager:
    def __init__(self, filename='all_time_high_scores.json'):
        self.filename = filename
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """Load high scores from the JSON file."""
        try:
            with open(self.filename, 'r') as file:
                high_scores = json.load(file)
                # Ensure the entries are tuples
                high_scores = [tuple(entry) if isinstance(entry, list) and len(entry) == 2 else self.handle_invalid_entry(entry) for entry in high_scores]
            logging.info(f"Loaded high scores: {high_scores}")
            return high_scores
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning("High scores file not found or invalid format. Starting with an empty list.")
            return []

    def save_high_scores(self, high_scores=None):
        """Save high scores to the file."""
        if high_scores is None:
            high_scores = self.high_scores
        try:
            with open(self.filename, 'w') as file:
                json.dump(high_scores, file)
            logging.info("High scores saved successfully.")
        except Exception as e:
            logging.error(f"Error saving high scores: {e}")

    def add_high_score(self, score):
        """Add a new high score with a valid timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score_with_timestamp = (score, timestamp)

        # Validate the score entry before adding
        if isinstance(score_with_timestamp, tuple) and len(score_with_timestamp) == 2:
            self.high_scores.append(score_with_timestamp)
        else:
            logging.warning(f"Attempted to add invalid score entry: {score_with_timestamp}")
            score_with_timestamp = self.handle_invalid_entry(score_with_timestamp)

        self.high_scores = sorted(self.high_scores, key=lambda x: x[0], reverse=True)[:5]  # Keep top 5 scores

        self.save_high_scores(self.high_scores)
        logging.info(f"New high score added: {score_with_timestamp}. Current scores: {self.high_scores}")

    def handle_invalid_entry(self, entry):
        """Handle invalid high score entries."""
        logging.warning(f"Invalid entry detected: {entry}. Assigning placeholder value.")
        return (0, "Invalid Timestamp")
