```markdown
# tetris8

tetris8 is a classic Tetris game implemented in Python using the Pygame library. Players can control falling tetromino pieces in a grid-based playing field, aiming to clear rows and achieve high scores. The game emphasizes modular design, allowing for future feature expansions.

## Overview 

The architecture of tetris8 consists of a main game loop that manages user input, updates the game state, and renders the grid and tetrominoes. The project is structured around key classes, including `Grid` for managing the playing field and `Tetromino` for representing the various tetromino shapes. The application is built using Python and the Pygame library, ensuring a modular design for future enhancements.

### Project Structure

- `main.py`: Initializes the game and runs the main loop.
- `tetris_game.py`: Contains the core game logic, including handling tetromino movement, scoring, and game over conditions.
- `grid.py`: Manages the grid state and collision detection for tetrominoes.
- `tetromino.py`: Defines the tetromino shapes and their properties.
- `Tests/`: Contains unit tests for the game's components.
- `requirements.txt`: Lists the project's dependencies.

## Features

- **Grid Creation**: A grid-based playing field where tetrominoes can move.
- **Tetromino Types**: Implements seven tetromino shapes (I, O, T, J, L, S, Z) with distinct colors.
- **Tetromino Movement**: Control tetrominoes using keyboard inputs (left, right, down, and rotation).
- **Collision Detection**: Prevents tetrominoes from moving outside the grid or overlapping with others.
- **Random Tetromino Generation**: Spawns a random tetromino at the start of the game.
- **Row Clearing**: Clears filled rows and updates the score.
- **Game Over Logic**: Ends the game when a tetromino cannot be placed.
- **High Score Tracking**: Displays the current score and tracks high scores for the session.

## Getting started

### Requirements

To run tetris8, you need the following installed on your computer:
- Python (version 3.9 or higher)
- Pygame library
- pytest (for testing)
- flake8 (for linting)

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Quickstart

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the game by executing the following command:

```bash
python main.py
```

### License

Copyright (c) 2024. All rights reserved.
```