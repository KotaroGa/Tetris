#!/usr/bin/env python3
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from tetris.game import Game
    print("✓ Game module imported successfully!")
    
    def main():
        """Main entry point for the Tetris game"""
        print("Starting Terminal Tetris...")
        print("Game is running! (Basic version)")
        print("Press Ctrl+C to exit")
        
        game = Game()
        game.run()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Current Python path:")
    for path in sys.path:
        print(f"  {path}")