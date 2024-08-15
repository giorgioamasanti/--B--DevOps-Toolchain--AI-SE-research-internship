```markdown
# Tetris8

Tetris8 is a classic Tetris game implemented in Python using the Pygame library. Players can control falling tetromino pieces on a grid-based playing field, aiming to clear rows and achieve high scores. The game emphasizes modularity and clear software design, allowing for future feature expansions.

## Overview

The architecture of Tetris8 consists of a main game loop that manages user input, updates the game state, and renders the grid and tetrominoes. The project is structured around key components such as the `Grid` class, which handles the grid state and collision detection, and the `Tetromino` class, which represents the different tetromino shapes and their movements. The application is built using Python and the Pygame library, ensuring a modular design for future feature expansions.

### Technologies

- **Python**: The programming language used to run the Tetris game.
- **Pygame**: A library for creating games in Python, handling graphics and user input.

### Project Structure

- `main.py`: The entry point of the application, initializing the game and running the main loop.
- `grid.py`: Contains the `Grid` class for managing the game grid and collision detection.
- `tetromino.py`: Defines the `Tetromino` class for the shapes and colors of tetrominoes.
- `tetris_game.py`: Implements the game logic and integrates the grid and tetromino functionality.
- `high_score_manager.py`: Manages high score tracking and storage.
- `all_time_high_scores.json`: Stores all-time high scores in a JSON format.
- `Tests/`: Contains unit and integration tests for various components of the game.
- `requirements.txt`: Lists the external dependencies required for the project.

## Features

- **Grid Creation**: A grid-based playing field where tetrominoes can move, defined by a fixed width and height (e.g., 10x20).
- **Tetromino Types**: Seven types of tetrominoes, each represented by distinct colors.
- **Tetromino Movement**: Control tetrominoes using keyboard inputs (left, right, down, rotate).
- **Random Tetromino Generation**: Spawn a random tetromino at the top of the grid at the start of the game.
- **Row Clearing**: Clear filled rows and update the score accordingly.
- **Game Over Condition**: End the game when a new tetromino cannot be placed.
- **High Score Tracking**: Maintain current session and all-time high scores, displayed in a user-friendly format.
- **Sound Effects and Music**: Background music and sound effects for an enhanced gaming experience.

## Getting started

### Requirements

- Python 3.x
- Pygame library
- Additional dependencies specified in `requirements.txt`

### Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tetris8.git
   cd tetris8
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

### License

Copyright (c) 2024. All rights reserved.
```