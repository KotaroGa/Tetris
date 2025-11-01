import curses
from .game import Game

def main(stdscr):
    """Main entry point for the Tetris game with curses"""

    # Create and run the game with the curses window
    game = Game(stdscr)
    game.run()

if __name__ == "__main__":
    # curses.wrapper handles curses initialization and cleanup automatically
    # Call the main function and pass the stdscr window
    curses.wrapper(main)