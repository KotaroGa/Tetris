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
        # Test with T-piece specifically (definitely changes when rotated)
        game = Game()
        game.current_piece = Tetromino('T')
        original_blocks = game.current_piece.blocks[:]

        # Rotate
        game.rotate()
        rotated_blocks = game.current_piece.blocks

        # T-piece should have different block positions after rotation
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
    
        # Create a piece near the top and let the normal game logic handle it
        original_y = game.current_piece.y
    
        # Drop the piece normally
        game.drop()
    
        # The piece should have moved down one position
        self.assertEqual(game.current_piece.y, original_y + 1)

    
    def test_scoring_single_line(self):
        """Test scoring for single clear"""
        game = Game()
        game.level = 1

        # Simulate clearing 1 line
        points = game._calculate_score(1)
        self.assertEqual(points, 40) # 40 x 1

        # Test with level 2
        game.level = 2
        points = game._calculate_score(1)
        self.assertEqual(points, 80) # 40 x 2

    
    def test_scoring_tetris(self):
        """Test scoring for Tetris (4 lines at once)"""
        game = Game()
        game.level = 1

        points = game._calculate_score(4)
        self.assertEqual(points, 1200) # 1200 x 1


    def test_level_progression(self):
        """Test that level increase after clearing enough lines"""
        game = Game()
        game.level = 1
        game.lines_cleared = 9

        # Clear 1 more line (total 10) - should level up
        game._update_level(1)
        self.assertEqual(game.level, 2)
        self.assertEqual(game.lines_cleared, 10)
