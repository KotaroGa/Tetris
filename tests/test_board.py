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
    
        # Move I-piece so bottom block is exactly at the bottom (y=19)
        # I-piece blocks at y=0: [(3,0), (4,0), (5,0), (6,0)] but wait this checks the real position
        print(f"\nI-piece shape: {tetromino.shape}")
        print(f"I-piece blocks at start: {tetromino.blocks}")
    
        # Move piece very low
        tetromino.y = 18  # This should definitely cause collision
        self.assertTrue(board.has_collision(tetromino))

    def test_collision_with_walls(self):
        ''' Test that tetromino hits walls'''
        board = Board()
        tetromino = Tetromino('I')

        # Move I-piece to left wall (I-piece wide is 4 blocks)
        tetromino.x = -1 # Partially off the left edge
        self.assertTrue(board.has_collision(tetromino))

        # Move I-piece to right wall
        tetromino.x = 7 # 10 -4 = 6 is max, so 7 is off edge(10 - 4 + 1 = 7)
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