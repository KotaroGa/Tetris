from  .config import TETROMINOS, COLORS

class Tetromino:
    '''
    Rrepresents a falling tetromino piece in the game
    Handles the shape, position, rotation and movement of a tetromino
    '''

    def __init__(self, shape_name: str):
        '''
        Initialize a new tetromino with the specified shape
        
        Args:
            shape_name (str): The shape type ('I), 'O', 'T', etc.')
        '''

        self.shape_name = shape_name # Store the shape indentifier
        self.shape = TETROMINOS[shape_name] # Get the 4x4 matrix for this shape
        self.color = COLORS[shape_name] # Get the terminal color
        self.x = 3 # Starting X position (centered on a 10-wide board)
        self.y = 0 # Starting Y position (top of the board)

    @property
    def blocks(self):
        '''
        Calculate the current positions of all blocks in this tetromino
        Returns a list of (x, y) coordinates for each block
        
        Returns:
            list: List of tuples representing block positions [(x1, y1), (x2, y2), ...]
        '''

        blocks = []
        # Loop through each row in the 4x4 shape matrix
        for y, row in enumerate(self.shape):
            # Loop through each column in the current row
            for x, cell in enumerate(row):
                if cell: # If this cell contains a block (value is 1)
                    # Calculate the actual board position by adding the tetromino's position

                    blocks.append((self.x + x, self.y + y))

        return blocks
    
    def rotate_clockwise(self):
        '''Rotate the tetromino 90 degrees clockwise '''
        # Transpose the matrix (rows become columns)
        transposed = list(zip(*self.shape))
        # Reverse each row to complete clockwise rotation
        self.shape = [list(reversed(row)) for row in transposed]

    def rotate_counter_clockwise(self):
        ''' Rotate the tetromino 90 degrees counter-clockwise '''
        # Reverse each row first
        reversed_rows = [list(reversed(row)) for row in self.shape]
        # Transpose the matrix
        self.shape = list(zip(*reversed_rows))