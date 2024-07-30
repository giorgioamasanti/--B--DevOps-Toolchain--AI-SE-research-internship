```markdown
# Tetris8

Tetris8 is a classic Tetris game implemented in Python using the Pygame library. Players can control falling tetromino pieces in a grid-based playing field using keyboard inputs. The project emphasizes modularity and clear software design, allowing for future feature expansions.

## Overview

The architecture of Tetris8 consists of a main game loop that manages user input, updates the game state, and renders the grid and tetrominoes. The project is structured around two primary classes: `Grid` and `Tetromino`. The `Grid` class handles the grid's state and collision detection, while the `Tetromino` class represents the different tetromino shapes and their movements. The application is built using Python and the Pygame library, ensuring a modular design for future feature expansions.

### Technologies

- **Python**: The programming language required to run the Tetris game.
- **Pygame**: A library for creating games in Python, used to handle graphics and user input.

### Project Structure

- `grid.py`: Defines the `Grid` class, which manages the grid structure and collision detection.
- `main.py`: Implements the main functionality and game loop for Tetris.
- `tetris_game.py`: Contains the `TetrisGame` class, which initializes the game and handles user interactions.
- `tetromino.py`: Defines the `Tetromino` class, representing the shapes and colors of tetrominoes.

## Features

- **Grid Creation**: A grid-based playing field (10x20) where tetrominoes can move.
- **Tetromino Types**: Implements seven types of tetrominoes (I, O, T, J, L, S, Z), each represented by a distinct color.
- **Tetromino Movement**: Players can control tetrominoes using keyboard inputs:
  - Left arrow key: Move tetromino left
  - Right arrow key: Move tetromino right
  - Down arrow key: Move tetromino down
  - Up arrow key: Rotate tetromino (optional for initial implementation)
- **Collision Detection**: Ensures tetrominoes do not move outside the grid or overlap with other tetrominoes.
- **Random Tetromino Generation**: At the start of the game, a random tetromino is spawned at the top of the grid.

## Getting started

### Requirements

To run the Tetris8 project, ensure you have the following installed on your computer:

- Python (version 3.x)
- Pygame library

### Quickstart

1. Clone the repository or download the project files.
2. Install the required dependencies by running:
   ```bash
   pip install pygame
   ```
3. Navigate to the project directory and run the game using:
   ```bash
   python main.py
   ```

### License

Copyright (c) 2024.
```