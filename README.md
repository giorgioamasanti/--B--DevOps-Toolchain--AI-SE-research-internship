```markdown
# tetris8

tetris8 is a classic Tetris game implemented in Python using the Pygame library. Players can control falling tetromino pieces within a grid-based playing field using keyboard inputs. The game emphasizes modularity and clear software design, allowing for future feature expansions.

## Overview

The architecture of the tetris8 project consists of a main game loop that manages user input, updates the game state, and renders the grid and tetrominoes. The project includes a `Grid` class for handling the grid's state and collision detection, and a `Tetromino` class that represents the different tetromino shapes and their movements. The application is structured to ensure modularity and ease of future enhancements.

### Technologies

- **Python**: The programming language used to develop the Tetris game.
- **Pygame**: A library that facilitates game development in Python, handling graphics and user input.

### Project Structure

- `main.py`: The main entry point for the game, initializing Pygame and running the game loop.
- `grid.py`: Contains the `Grid` class for managing the grid layout and collision detection.
- `tetromino.py`: Defines the `Tetromino` class, representing the shapes and colors of tetrominoes.
- `tetris_game.py`: Implements the game logic, including tetromino movement and scoring.
- `Tests/`: Contains unit tests for various components of the game to ensure functionality and correctness.

## Features

- **Grid Creation**: A grid-based playing field (10x20) where tetrominoes can move.
- **Tetromino Types**: Seven distinct tetromino shapes (I, O, T, J, L, S, Z), each represented by a unique color.
- **Tetromino Movement**: Players can control tetrominoes using the arrow keys to move left, right, down, and rotate.
- **Random Tetromino Generation**: A new tetromino is spawned at the top of the grid at the start of each game.
- **Row-Clearing Functionality**: Rows are cleared when filled, and the score increases accordingly.
- **Game Over State**: The game ends when a new tetromino cannot be placed due to collisions, displaying a "Game Over" message.
- **High Score Tracking**: Tracks and displays the top scores for the current session, along with timestamps.

## Getting started

### Requirements

To run the project, ensure you have the following installed on your computer:
- Python (version 3.x)
- Pygame library (install via `pip install pygame`)

### Quickstart

1. Clone the repository or download the project files.
2. Navigate to the project directory in your terminal.
3. Run the game using the command:
   ```bash
   python main.py
   ```
4. Use the arrow keys to control the tetrominoes and enjoy the game!

### License

Copyright (c) 2024.
```