import unittest
from src.tetris.tetromino import Tetromino 
from src.tetris.config import TETROMINOS 

class TestTetromino(unittest.TestCase):
    # Test cases for the Tetromino class -testing each tetromino shape

    def test_tetromino_creation(self):
        # Test that we can create each tetromino type successfully
        '''Loop through all tetromino shapes defined in config (I, O, T, etc.)'''
        for shape_name in TETROMINOS.keys():
            # Create a tetromino instance for htis shape
            tetromino = Tetromino(shape_name)
            # Verify the shape name was set correctly
            self.assertEqual(tetromino.shape_name, shape_name)

    def test_tetromino_has_correct_blocks(self):
        # Test that each tetromino has exactly 4 blocks
        '''Create an I shaped tetromino'''
        tetromino = Tetromino('I')
        # A tetromino should always have exactly 4 blocks+
        self.assertEqual(len(tetromino.blocks), 4)

        