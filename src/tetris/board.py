from .config import BOARD_HEIGHT, BOARD_WIDTH

class Board:
    '''
    Represents the Tetris game board - a grid where tetrominos fall and stack.
    
    The board is responsible for:
    - Tracking fixed blocks on the playing field
    - Collision detection for moving tetrominos
    - Line clearing when rows are complete
    - Locking tetrominos in place when they land
    
    Attributes:
        width (int): Number of columns (usually 10)
        height (int): Number of rows (usually 20)
        grid (list): 2D list representing occupied cells
    '''

    def __init__(self):
        ''' Initialize an empty game board '''
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def has_collision(self, tetromino):
        '''
        Check if given tetromino collides with board boundaries or placed blocks
        
        Args:
            tetromino (Tetromino): The tetromino to check for collisions
        
        Returns:
            bool: True if collision detected, False otherwise
        '''
        for block_x, block_y in tetromino.blocks:
            # Check if block is outside left/right boundaries
            if block_x < 0 or block_x >= self.width:
                return True
            # Check if block is below the bottom
            if block_y >= self.height:
                return True
            # check if block overlaps with already placed blocks (Not yet implemented, first add block placement)

        return False