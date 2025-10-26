import unittest
import sys
import os

# Add src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris.board import Board
from tetris.tetromino import Tetromino

class TestBoard(unittest.TestCase):

    def test_board_creation(self):
        ''' Test that board is created with correct dimensions'''
        board = Board()
        # Board should have correct width and height
        self.assertEqual(board.width, 10)
        self.assertEqual(board.height, 20)
        # Board should start empty(all cells = 0 or None)
        self.assertEqual(len(board.grid), 20) # 20 rows
        self.assertEqual(len(board.grid[0]), 10) # 10 columns


    def test_board_starts_empty(self):
        """Test that all board cells start as empty"""
        board = Board()
        # Check that all cells are empty (0 or None)
        for row in board.grid:
            for cell in row:
                self.assertFalse(cell)  # Should be falsy (0, None, False)


    def test_collision_with_floor(self):
        """Test that collision is detected when piece hits bottom"""
        board = Board()
        tetromino = Tetromino('I')
    
        # Debug: see where blocks are
        print(f"\nI-piece blocks at start: {tetromino.blocks}")
    
        # Move I-piece so bottom blocks hit the bottom
        # Bottom of board is y=19 (we have 20 rows: 0-19)
        # I-piece blocks are at y=1 in the matrix.
        # tetromino.y + 1 = actual y position of bottom blocks
        # We want: tetromino.y + 1 = 19  → tetromino.y = 18
        tetromino.y = 18
    
        print(f"I-piece blocks at y=18: {tetromino.blocks}")
    
        # At y=18, bottom blocks should be at y=19 (the last row)
        self.assertFalse(board.has_collision(tetromino))
    
        # Should collide
        tetromino.y = 19
        print(f"I-piece blocks at y=19: {tetromino.blocks}")
        self.assertTrue(board.has_collision(tetromino))


    def test_collision_with_walls(self):
        """Test that collision is detected with left/right walls"""
        board = Board()
        tetromino = Tetromino('I')
    
        print(f"\nI-piece blocks at start: {tetromino.blocks}")
    
        # Move I-piece to left wall
        # I-piece leftmost blocks are at x=3 in the matrix
        # We want: tetromino.x + 3 < 0
        tetromino.x = -1
        print(f"I-piece blocks at x=-1: {tetromino.blocks}")
        self.assertTrue(board.has_collision(tetromino))
    
        # Reset and test right wall
        tetromino = Tetromino('I')
        # I-piece rightmost blocks are at x=6 in the matrix
        # We want: tetromino.x + 6 >= 10
        tetromino.x = 7  # 7 + 6 = 13 which is >= 10
        print(f"I-piece blocks at x=7: {tetromino.blocks}")
        self.assertTrue(board.has_collision(tetromino))


    def test_no_collision_valid_position(self):
        ''' Test that no collision is detected in valid positions '''
        board = Board()
        tetromino = Tetromino('I')

        # Starting position should be valid
        self.assertFalse(board.has_collision(tetromino))

        # Various valid positions
        tetromino.x = 3
        tetromino.y = 5
        self.assertFalse(board.has_collision(tetromino))        


    def test_debug_block_positions(self):
        """Debug method to see where blocks actually are"""
        board = Board()
        tetromino = Tetromino('I')
    
        print(f"\nI-piece blocks at start: {tetromino.blocks}")
    
        tetromino.y = 17
        print(f"I-piece blocks at y=17: {tetromino.blocks}")
    
        # Check each block individually
        for x, y in tetromino.blocks:
            print(f"Block at ({x}, {y}): x_ok={0 <= x < 10}, y_ok={0 <= y < 20}")

    def test_collision_with_placed_blocks(self):
        ''' Test that collision is detected with already placed blocks '''
        board = Board()
        tetromino = Tetromino('I')

        # Place a block manually in the board grid
        board.grid[5][5] = 1 # Place a block at (5, 5)

        # Position tetromino to collide with the placed block
        tetromino.x = 4
        tetromino.y = 4
        # I-piece at this position should have a block at (5, 5)

        self.assertTrue(board.has_collision(tetromino))