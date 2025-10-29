# Terminal Tetris - Architecture Overview

## Project Structure

terminal-tetris/
├── src/tetris/ # Source code
├── tests/ # Unit tests
├── docs/ # Documentation (you are here!)
└── requirements.txt # Python dependencies


## Core Components

### Tetromino (`src/tetris/tetromino.py`)
Represents the falling pieces in the game.

**Responsibilities:**
- Store the shape and type (I, O, T, L, J, S, Z)
- Handle rotation (clockwise/counter-clockwise)
- Track current position on the board
- Provide block coordinates for rendering and collision detection

**Key Methods:**
- `rotate_clockwise()` - Rotate 90° right
- `rotate_counter_clockwise()` - Rotate 90° left
- `blocks` property - Get current block positions

### Board (`src/tetris/board.py`) - *In Development*
The game grid where tetrominos fall and stack.

**Responsibilities:**
- Maintain the 10x20 game grid
- Detect collisions between tetrominos and placed blocks
- Lock tetrominos in place when they land
- Clear completed lines and collapse the board

### Game Engine (`src/tetris/game.py`) - *Planned*
The main game loop and state manager.

### Renderer (`src/tetris/renderer.py`) - *Planned*
Handles terminal display and user interface.

## Development Workflow
We follow GitFlow with Test-Driven Development (TDD):
1. Write failing tests first
2. Implement minimal code to pass tests
3. Refactor and improve
4. Commit to feature branches
5. Merge to develop when complete