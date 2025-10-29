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
        for shape_name in ['I', 'O', 'T', 'L', 'J', 'S', 'Z']:  # Test ALL shapes
            with self.subTest(shape=shape_name):
                tetromino = Tetromino(shape_name)
                self.assertEqual(tetromino.shape_name, shape_name)
    

    def test_all_tetrominos_have_correct_blocks(self):
        """Test that ALL tetrominos have exactly 4 blocks"""
        for shape_name in ['I', 'O', 'T', 'L', 'J', 'S', 'Z']:
            with self.subTest(shape=shape_name):
                tetromino = Tetromino(shape_name)
                self.assertEqual(len(tetromino.blocks), 4, 
                               f"{shape_name} piece should have 4 blocks")


    def test_rotation_changes_positions(self):
        """Test that rotation changes block positions for relevant shapes"""
        # Test shapes that actually change when rotated
        for shape_name in ['I', 'T', 'L', 'J', 'S', 'Z']:
            with self.subTest(shape=shape_name):
                tetromino = Tetromino(shape_name)
                original_blocks = tetromino.blocks[:]
                
                tetromino.rotate_clockwise()
                rotated_blocks = tetromino.blocks
                
                self.assertEqual(len(rotated_blocks), 4)
                self.assertNotEqual(rotated_blocks, original_blocks,
                                  f"{shape_name} piece should change position when rotated")


    def test_o_piece_rotation_unchanged(self):
        """Test that O-piece rotation doesn't change block positions (it's a square)"""
        tetromino = Tetromino('O')
        original_blocks = tetromino.blocks[:]
        
        tetromino.rotate_clockwise()
        rotated_blocks = tetromino.blocks
        
        # O-piece should look the same after rotation (it's symmetric)
        self.assertEqual(rotated_blocks, original_blocks)


    def test_all_tetromino_shapes_exist(self):
        """Test that all 7 classic tetromino shapes are available"""
        expected_shapes = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        
        for shape_name in expected_shapes:
            with self.subTest(shape=shape_name):
                tetromino = Tetromino(shape_name)
                self.assertEqual(tetromino.shape_name, shape_name)
                # Each tetromino should have exactly 4 blocks
                self.assertEqual(len(tetromino.blocks), 4)


    def test_tetromino_rotation_all_shapes(self):
        """Test that all tetromino shapes can rotate properly multiple times"""
        for shape_name in ['I', 'O', 'T', 'L', 'J', 'S', 'Z']:
            with self.subTest(shape=shape_name):
                tetromino = Tetromino(shape_name)
                
                # Rotate 4 times should return to original orientation
                original_blocks = tetromino.blocks[:]
                
                for _ in range(4):
                    tetromino.rotate_clockwise()
                
                final_blocks = tetromino.blocks
                self.assertEqual(len(final_blocks), 4)
                # After 4 rotations, should be back to original
                self.assertEqual(final_blocks, original_blocks)
