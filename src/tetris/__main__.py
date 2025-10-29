from .game import Game

def main():
    """Main entry point for the Tetris game"""
    print("Starting Terminal Tetris...")
    print("Controls: We'll add these in the next feature!")
    print("Press Ctrl+C to exit")
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()