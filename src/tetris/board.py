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
            # check if block overlaps with already placed blocks
            if block_y >= 0 and self.grid[block_y][block_x]:
                return True

        return False
    

    def lock_tetromino(self, tetromino):
        '''
        Lock a tetromino onto the board, making it part of the fixed blocks
        
        Args:
            tetromino (Tetromino): The tetromino to lock in place
            
        Raises:
            ValueError: if the tetromino is in an invalid position
        '''
        if self.has_collision(tetromino):
            raise ValueError("Cannot lock tetromino - position would cause collision")
        
        # Place each block of the tetromino on the board
        for block_x, block_y in tetromino.blocks:
            if 0 <= block_y < self.height and 0 <= block_x < self.width:
                self.grid[block_y][block_x] = tetromino.color


    def get_complete_lines(self):
        """Find all rows that completely filled with blocks"""
        complete_lines = []
        for y in range(self.height):
            # Check if every cell in this row is filled out (not 0)
            if all(cell != 0 for cell in self.grid[y]):
                complete_lines.append(y)
        return complete_lines
    
    def clear_lines(self):
        """ Clear all complete lines and make blocks above fall down """
        complete_lines = self.get_complete_lines()

        if not complete_lines:
            return 0
        
        # Sort from top to bottom for proper clearing
        complete_lines.sort()

        # Remove each complete line and shift everything down
        for line_y in complete_lines:
            # Remove the complete line
            self.grid.pop(line_y)
            # Add a new empty line at the top
            self.grid.insert(0, [0] * self.width)

        return len(complete_lines)