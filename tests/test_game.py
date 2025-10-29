import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris.game import Game
from tetris.tetromino import Tetromino

class TestGame(unittest.TestCase):
    
    def test_game_initialization(self):
        """Test that game initializes with correct default state"""
        game = Game()
        
        # Should have a board
        self.assertEqual(game.board.width, 10)
        self.assertEqual(game.board.height, 20)
        
        # Should start with a current tetromino
        self.assertIsNotNone(game.current_piece)
        self.assertIsInstance(game.current_piece, Tetromino)
        
        # Should start with score 0 and level 1
        self.assertEqual(game.score, 0)
        self.assertEqual(game.level, 1)
        
        # Game should not be over at start
        self.assertFalse(game.game_over)
    
    def test_game_movement(self):
        """Test that pieces can be moved left/right"""
        game = Game()
        original_x = game.current_piece.x
        
        # Move right
        game.move_right()
        self.assertEqual(game.current_piece.x, original_x + 1)
        
        # Move left (back to original)
        game.move_left()
        self.assertEqual(game.current_piece.x, original_x)
    
    def test_game_rotation(self):
        """Test that pieces can be rotated"""
        game = Game()
        original_blocks = game.current_piece.blocks[:]
        
        # Rotate
        game.rotate()
        rotated_blocks = game.current_piece.blocks
        
        # Should still have 4 blocks, but positions changed
        self.assertEqual(len(rotated_blocks), 4)
        self.assertNotEqual(rotated_blocks, original_blocks)
    
    def test_game_drop(self):
        """Test that pieces can be dropped"""
        game = Game()
        original_y = game.current_piece.y
        
        # Drop one step
        game.drop()
        
        # Should move down one position
        self.assertEqual(game.current_piece.y, original_y + 1)
    
    def test_piece_locking(self):
        """Test that pieces lock when they hit bottom"""
        game = Game()
        
        # Move piece to near bottom
        game.current_piece.y = 18  # Near bottom for most pieces
        
        # Drop until it locks
        for _ in range(5):  # Should lock within a few drops
            game.drop()
            if game.current_piece.y == 0:  # New piece spawned
                break
        
        # Should have a new current piece
        self.assertEqual(game.current_piece.y, 0)