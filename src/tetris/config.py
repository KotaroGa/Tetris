'''
Game configuration and constants
This file contains all the game settings that might need adjustment
'''

# Tetromino shapes defined as 4x4 matrices
# 1 represents a block, 0 represents empty space
# Each shape is defined in its initial rotation state

TETROMINOS = {
    'I': [ # The straight line piece (cyan)
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    'O': [ # The square piece (yellow)
        [0, 0, 0, 0],
        [0, 1, 1, 0], # 2x2 square
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    'T': [ # The T-shape piece (magenta)
        [0, 0, 0, 0],
        [0, 1, 0, 0], # T shape: three across, one down the middel
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ],
     # L, J, S, Z will be added later, right now let's get the basics working
}

# Board dimensions -standard Tetris board is 10 blocks wide, 20 blocks tall
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Terminal color codes for each tetromino type
# These are ANSI color codes that work in most terminals
COLORS = {
    'I': 36, # Cyan
    'O': 33, # Yellow
    'T': 35, # Magenta
    'L': 94, # Bright Yellow (looks orange)
    'J': 34, # Blue
    'S': 32, #Green
    'Z': 31, #Red
}

