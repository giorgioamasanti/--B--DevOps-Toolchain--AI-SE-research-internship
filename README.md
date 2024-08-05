```markdown
# tetris8

Tetris8 is a classic Tetris game implemented in Python using the Pygame library. Players can control falling tetromino pieces in a grid-based playing field, utilizing keyboard inputs to manipulate the pieces while aiming to clear rows and achieve high scores.

## Overview

The architecture of Tetris8 consists of a main game loop that manages user input, updates the game state, and renders the grid and tetrominoes. The project is structured around key classes, including the `Grid` class for managing the grid state and collision detection, and the `Tetromino` class for representing various tetromino shapes and their movements. The application is built using Python and the Pygame library, ensuring a modular design that allows for future feature expansions.

### Technologies Used
- **Python**: The programming language used to implement the game.
- **Pygame**: A library for creating games in Python, used for handling graphics and user input.

### Project Structure
- `main.py`: Entry point of the game, initializing Pygame and running the main game loop.
- `grid.py`: Defines the `Grid` class for managing the game grid and collision detection.
- `tetromino.py`: Defines the `Tetromino` class for managing tetromino shapes and colors.
- `tetris_game.py`: Implements the core game logic and state management.
- `Tests/`: Contains unit tests for various components of the game.

## Features

- **Grid Creation**: A grid-based playing field defined by a fixed width and height (e.g., 10x20) where tetrominoes can move.
- **Tetromino Types**: Includes various tetromino shapes (I, O, T, J, L, S, Z), each represented by distinct colors.
- **Tetromino Movement**: Players can control tetrominoes using keyboard inputs (left, right, down, and rotate).
- **Collision Detection**: Prevents tetrominoes from moving outside the grid boundaries or overlapping with others.
- **Random Tetromino Generation**: Spawns a random tetromino at the start of the game.
- **Row-Clearing Functionality**: Clears filled rows and updates the score accordingly.
- **Game Over Condition**: Ends the game when a new tetromino cannot be placed upon spawning.
- **High Score Tracking**: Displays the current score and maintains a high score table for the session.

## Getting started

### Requirements

- Python 3.x
- Pygame library (install via pip: `pip install pygame`)

### Quickstart

1. Clone the repository or download the project files.
2. Navigate to the project directory in your terminal.
3. Run the game using the command:
   ```bash
   python main.py
   ```
4. Use the arrow keys to control the tetromino pieces:
   - Left Arrow: Move left
   - Right Arrow: Move right
   - Down Arrow: Move down
   - Up Arrow: Rotate tetromino (anticlockwise)

### License

Copyright (c) 2024.
```