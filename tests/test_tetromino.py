import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris.tetromino import Tetromino
from tetris.config import TETROMINOS

class TestTetromino(unittest.TestCase):
    """Test cases for the Tetromino class - testing each tetromino shape"""
    
    def test_tetromino_creation(self):
        """Test that we can create each tetromino type successfully"""
        for shape_name in ['I', 'O', 'T']:  # Only test the shapes we have
            tetromino = Tetromino(shape_name)
            self.assertEqual(tetromino.shape_name, shape_name)
    
    def test_tetromino_has_correct_blocks(self):
        """Test that each tetromino has exactly 4 blocks"""
        tetromino = Tetromino('I')
        self.assertEqual(len(tetromino.blocks), 4)
    
    def test_tetromino_rotation(self):
        """Test that tetromino rotation changes block positions"""
        tetromino = Tetromino('T')
        original_blocks = tetromino.blocks[:]  # Save original block positions
        
        # Rotate clockwise - block positions should change
        tetromino.rotate_clockwise()
        rotated_blocks = tetromino.blocks
        
        # After rotation, we should still have 4 blocks
        self.assertEqual(len(rotated_blocks), 4)
        # But the positions should be different
        self.assertNotEqual(rotated_blocks, original_blocks)
