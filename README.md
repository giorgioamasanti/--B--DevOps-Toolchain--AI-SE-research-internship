```markdown
# tetris8

tetris8 is a classic Tetris game implemented in Python using the Pygame library. Players can control falling tetromino pieces in a grid-based playing field, utilizing keyboard inputs to maneuver the pieces and clear rows.

## Overview

The architecture of tetris8 consists of a main game loop that manages user input, updates the game state, and renders the grid and tetrominoes. Key components include a `Grid` class for managing the grid's state and collision detection, and a `Tetromino` class for representing various tetromino shapes and their movements. This modular design facilitates future feature expansions.

The project structure includes:
- `main.py`: Entry point for the game.
- `grid.py`: Contains the `Grid` class for grid management.
- `tetromino.py`: Defines the `Tetromino` class for tetromino shapes.
- `tetris_game.py`: Implements the main game logic and rendering.
- `Tests/`: Directory containing unit tests for the game components.

## Features

- **Grid Creation**: A fixed-width and height grid (e.g., 10x20) for tetromino movement.
- **Tetromino Types**: Seven distinct tetromino shapes (I, O, T, J, L, S, Z), each with a unique color.
- **Tetromino Movement**: Control tetrominoes using arrow keys (left, right, down) and rotate using the up arrow key.
- **Random Tetromino Generation**: A new random tetromino spawns at the top of the grid at the start of the game.
- **Row-Clearing Functionality**: Clear filled rows and update the score accordingly.
- **Game Over Condition**: The game ends when a new tetromino cannot be placed due to collisions, displaying a "Game Over" message.

## Getting started

### Requirements

- Python (version 3.6 or higher)
- Pygame library (install via `pip install pygame`)

### Quickstart

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Run the game using the command:
   ```bash
   python main.py
   ```
4. Use the arrow keys to control the tetrominoes.

### License

Copyright (c) 2024.
```