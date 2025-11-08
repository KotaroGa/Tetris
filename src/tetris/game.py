from .board import Board
from .tetromino import Tetromino
from .config import BOARD_WIDTH, BOARD_HEIGHT
import random
import time
import curses

class Game:
    """
    Main game controller - manages the game loop, state, and user input.
    
    The game loop follows this pattern:
    1. Process input (move, rotate, drop)
    2. Update game state (gravity, collisions, scoring)
    3. Render the game display
    4. Repeat until game over
    """
    stdscr: 'curses._CursesWindow' # type: ignore 

    def __init__(self, stdscr=None):  # Add stdscr parameter
        """
        Initialize a new Tetris game
        
        Args:
            stdscr: curses window object (None for testing)
        """
        self.stdscr = stdscr  # Store the curses window
        self.board = Board()
        self.current_piece = self._create_new_piece()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.lines_cleared = 0
        self.last_drop_time = time.time()
        self.drop_interval = 1.0  # Pieces fall every 1 second initially
        
        # Initialize curses if we have a window
        if self.stdscr:
            self._init_curses()
    
    def _init_curses(self):
        """Initialize curses settings for the game"""
        # Don't wait for Enter key - get input immediately
        self.stdscr.nodelay(True)
        # Don't echo typed characters to the screen
        curses.noecho()
        # Enable special keys (arrow keys, etc.)
        self.stdscr.keypad(True)
        # Hide the cursor
        curses.curs_set(0)
    
    def _check_window_size(self):
        """Check if the terminal window is large enough to display the game"""
        if not self.stdscr:
            return True # No check needed without curses
        
        # Terminal dimensions
        height, width = self.stdscr.getmaxyx()
        required_height = 2 + self.board.height + 2 + 3
        required_width = 5 + self.board.width * 2 + 2 # Board width +  borders

        if height < required_height or width < required_width:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, 'Terminal too small!')
            self.stdscr.addstr(1, 0, f'Required: {required_width}x{required_height}')
            self.stdscr.addstr(2, 0, f'Current: {width}x{height}')
            self.stdscr.addstr(3, 0, 'Please resize your terminal and restart.')
            self.stdscr.refresh()
            return False
        
        return True

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
        if self.board.has_collision(self.current_piece):
            # If collision, rotate back
            self.current_piece.rotate_counter_clockwise()
    
    def drop(self):
        """Move current piece down one step and check for locking"""
        self.current_piece.y += 1
        if self.board.has_collision(self.current_piece):
            # If collision after dropping, lock the piece
            self.current_piece.y -= 1  # Undo the last move
            self._lock_piece()
    
    def hard_drop(self):
        """
        Drop the piece all the way to the bottom instantly
        """
        # Keep dropping until we hit something
        while not self.board.has_collision(self.current_piece):
            self.current_piece.y += 1
        
        # We went one step too far, so go back one
        self.current_piece.y -= 1
        # Lock the piece in place
        self._lock_piece()
    
    def _lock_piece(self):
        """Lock the current piece and create a new one"""
        self.board.lock_tetromino(self.current_piece)

        # Clear lines and calculate score
        lines_cleared = self.board.clear_lines()
        if lines_cleared > 0:
            # Use our scoring system
            points_earned = self._calculate_score(lines_cleared)
            self.score += points_earned
            self._update_level(lines_cleared)

        self.current_piece = self._create_new_piece()
        
        # Check if game over (new piece collides immediately)
        if self.board.has_collision(self.current_piece):
            self.game_over = True
    
    def _apply_gravity(self):
        """Make the current piece fall automatically based on time"""
        current_time = time.time()
        if current_time - self.last_drop_time > self.drop_interval:
            self.drop()
            self.last_drop_time = current_time
    
    def handle_input(self):
        """
        Process keyboard input using curses
        
        Returns:
            bool: True if the game should continue, False if should exit
        """
        if not self.stdscr:
            return True  # No input handling without curses
            
        try:
            # Get the pressed key (non-blocking)
            key = self.stdscr.getch()
            
            # If no key was pressed, getch returns -1
            if key == -1:
                return True
                
            # Handle different keys
            if key == ord('q') or key == ord('Q'):
                return False  # Quit game
            elif key == curses.KEY_LEFT:
                self.move_left()
            elif key == curses.KEY_RIGHT:
                self.move_right()
            elif key == curses.KEY_DOWN:
                self.drop()
            elif key == curses.KEY_UP:
                self.rotate()
            elif key == ord(' '):  # Spacebar for hard drop
                self.hard_drop()
            elif key == ord('r') or key == ord('R'):
                self.rotate()
                
        except Exception as e:
            # If there's an input error, just continue the game
            return True
            
        return True

    def update(self):
        """Update game state - called every frame"""
        if self.game_over:
            return
        
        # Apply automatic gravity
        self._apply_gravity()
    
    def render(self):
        """Render the current game state to terminal"""
        if not self.stdscr:
            # Fallback to simple print rendering
            self._render_simple()
            return
        
        try:
            # Clear the screen
            self.stdscr.clear()
        
            # Simple header that fits in small terminals
            self._safe_addstr(0, 0, "TETRIS - Q:Quit Arrows:Move R:Rotate Space:Drop")
        
            # Calculate minimal board position
            start_x = 2
            start_y = 2
        
            # Draw top border
            self._safe_addstr(start_y - 1, start_x - 1, "+" + "-" * self.board.width * 2 + "+")
        
            # Create a display grid
            display_grid = [row[:] for row in self.board.grid]
        
            # Add current piece to display
            for x, y in self.current_piece.blocks:
                if 0 <= y < self.board.height and 0 <= x < self.board.width:
                    display_grid[y][x] = 1  # Use simple 1 for current piece
        
            # Draw each row
            for y in range(min(20, self.board.height)):  # Limit to 20 rows max
                if start_y + y >= curses.LINES - 5:  # Don't draw beyond screen
                    break
                
                self._safe_addstr(start_y + y, start_x - 1, "|")
                for x in range(self.board.width):
                    if display_grid[y][x]:
                        self._safe_addstr(start_y + y, start_x + x * 2, "[]")
                    else:
                        self._safe_addstr(start_y + y, start_x + x * 2, "  ")
                self._safe_addstr(start_y + y, start_x + self.board.width * 2, "|")
        
            # Draw bottom border if we have space
            if start_y + min(20, self.board.height) < curses.LINES - 2:
                self._safe_addstr(start_y + min(20, self.board.height), start_x - 1, "+" + "-" * self.board.width * 2 + "+")
        
            # Simple game info
            info_line = start_y + min(20, self.board.height) + 2
            if info_line < curses.LINES:
                self._safe_addstr(info_line, 0, f"Score:{self.score} Level:{self.level} Lines:{self.lines_cleared}")
        
            if self.game_over and info_line + 1 < curses.LINES:
                self._safe_addstr(info_line + 1, 0, "GAME OVER!")
        
            self.stdscr.refresh()
        
        except Exception as e:
            # If anything fails, use simple rendering
            curses.endwin()
            self.stdscr = None
            self._render_simple()

    def _render_simple(self):
        """Fallback rendering without curses (for testing or when curses fails)"""
        # Simple text-based rendering
        print("\033[2J\033[H")  # Clear screen and move cursor to top
    
        print("🎮 TERMINAL TETRIS 🎮")
        print("Controls: ← → ↓ Move | ↑/R Rotate | Space Hard Drop | Q Quit")
        print()
    
        # Create a display grid that combines board and current piece
        display_grid = [row[:] for row in self.board.grid]
    
        # Add current piece to display
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
        print(f"Score: {self.score}")
        print(f"Level: {self.level}") 
        print(f"Lines: {self.lines_cleared}")
    
        if self.game_over:
            print("GAME OVER!")        

    def _safe_addstr(self, y, x, text, attributes=0):
        """Safely add text to the curses window, handling boundary errors"""
        if not self.stdscr:
            return
        
        try:
            max_y, max_x = self.stdscr.getmaxyx()
            # Check if position is within window bounds and text fits
            if (0 <= y < max_y and 0 <= x < max_x and 
                x + len(text) <= max_x):
                self.stdscr.addstr(y, x, text, attributes)
                return True
            return False
        except curses.error:
            return False
    
    def run(self):
        """Main game loop using curses"""
        try:
            # Try to run with curses
            if self.stdscr:
                while not self.game_over:
                    if not self.handle_input():
                        break
                    self.update()
                    self.render()
                    time.sleep(0.05)
            else:
                # Fallback to simple mode
                self._run_simple()
            
        except KeyboardInterrupt:
            pass  # User pressed Ctrl+C
        except Exception as e:
            # If curses fails, fall back to simple mode
            if self.stdscr:
                curses.endwin()
                self.stdscr = None
            self._run_simple()
        finally:
            # Clean up curses when game ends
            if self.stdscr:
                try:
                    curses.endwin()
                except:
                    pass

    def _run_simple(self):
        """Fallback game loop without curses"""
        print("Running in simple mode (no keyboard controls)")
        while not self.game_over:
            self.update()
            self._render_simple()
            time.sleep(0.5)  # Slower for readability


    def _calculate_score(self, lines_cleared):
        """
        Calculate score based on authentic Tetris scoring system
        
        Args:
            lines_cleared (int): Number of lines cleared at once (1-4)

        Returns:
            int: Points earned
        """
        # Classic NES Tetris scoring
        scoring_table = {
            1: 40,   # 1 line = 40 points
            2: 100,  # 2 lines = 100 points
            3: 300,  # 3 lines = 300 points
            4: 1200, # 4 lines = 1200 points (Tetris)
        }

        base_points = scoring_table.get(lines_cleared, 0)
        return base_points * self.level
    

    def _update_level(self, new_lines_cleared):
        """
        Update level based on total lines cleared

        Args:
            new_lines_cleared (int): Lines cleared in the current move
        """
        self.lines_cleared += new_lines_cleared
        # Level up every 10 lines (classic Tetris progression)
        self.level = (self.lines_cleared // 10) + 1

        # Increase game speed with level (every level = 10% faster)
        self.drop_interval = max(0.1, 1.0 - (self.level -1) * 0.1)
