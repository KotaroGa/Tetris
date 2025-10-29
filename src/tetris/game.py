from .board import Board
from .tetromino import Tetromino
from .config import BOARD_WIDTH, BOARD_HEIGHT
import random
import time

class Game:
    """
    Main game controller - manages the game loop, state, and user input.
    
    The game loop follows this pattern:
    1. Process input (move, rotate, drop)
    2. Update game state (gravity, collisions, scoring)
    3. Render the game display
    4. Repeat until game over
    """
    
    def __init__(self):
        """Initialize a new Tetris game"""
        self.board = Board()
        self.current_piece = self._create_new_piece()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.lines_cleared = 0
        self.last_drop_time = time.time()
        self.drop_interval = 1.0  # Pieces fall every 1 second initially
    
    def _create_new_piece(self):
        """Create a new random tetromino at the top center"""
        shapes = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        shape = random.choice(shapes)
        tetromino = Tetromino(shape)
        # Center the piece at the top
        tetromino.x = BOARD_WIDTH // 2 - 2  # Rough center for 4x4 pieces
        tetromino.y = 0
        return tetromino
    
    def move_left(self):
        """Move current piece left if possible"""
        self.current_piece.x -= 1
        if self.board.has_collision(self.current_piece):
            self.current_piece.x += 1  # Undo move if collision
    
    def move_right(self):
        """Move current piece right if possible"""
        self.current_piece.x += 1
        if self.board.has_collision(self.current_piece):
            self.current_piece.x -= 1  # Undo move if collision
    
    def rotate(self):
        """Rotate current piece clockwise if possible"""
        self.current_piece.rotate_clockwise()
    
    def drop(self):
        """Move current piece down one step and check for locking"""
        self.current_piece.y += 1
        if self.board.has_collision(self.current_piece):
            # If collision after dropping, lock the piece
            self.current_piece.y -= 1  # Undo the last move
            self._lock_piece()
    
    def _lock_piece(self):
        """Lock the current piece and create a new one"""
        self.board.lock_tetromino(self.current_piece)
        self.current_piece = self._create_new_piece()  # This line is correct
    
        # Check if game over (new piece collides immediately)
        if self.board.has_collision(self.current_piece):
            self.game_over = True
    
    def _apply_gravity(self):
        """Make the current piece fall automatically based on time"""
        current_time = time.time()
        if current_time - self.last_drop_time > self.drop_interval:
            self.drop()
            self.last_drop_time = current_time
    
    def update(self):
        """Update game state - called every frame"""
        if self.game_over:
            return
        
        # Apply automatic gravity
        self._apply_gravity()
    
    def render(self):
        """Render the current game state to terminal"""
        # Simple text-based rendering for now
        print("\033[2J\033[H")  # Clear screen and move cursor to top
    
        # Create a display grid that combines board and current piece
        display_grid = [row[:] for row in self.board.grid]
    
        # Add current piece to display - FIXED: use board.height and board.width
        for x, y in self.current_piece.blocks:
            if 0 <= y < self.board.height and 0 <= x < self.board.width:
                display_grid[y][x] = self.current_piece.color
    
        # Print the board
        print("+" + "-" * (self.board.width * 2) + "+")
        for row in display_grid:
            print("|", end="")
            for cell in row:
                if cell:
                    print("██", end="")  # Block
                else:
                    print("  ", end="")  # Empty space
            print("|")
        print("+" + "-" * (self.board.width * 2) + "+")
    
        # Print game info
        print(f"Score: {self.score} | Level: {self.level} | Lines: {self.lines_cleared}")
        if self.game_over:
            print("GAME OVER!")
    
    def run(self):
        """Main game loop"""
        try:
            while not self.game_over:
                self.update()
                self.render()
                time.sleep(0.1)  # Control loop speed
        except KeyboardInterrupt:
            print("\nGame stopped by user")
