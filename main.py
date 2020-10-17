import pygame
import gui
import os
import tkinter as tk

# Get screen dimensions
root = tk.Tk()
root.withdraw()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

# Create grid dimensions
SQUAREWIDTH = 20  # input()
XSQUARES = 20  # input()
YSQUARES = 20  # input()

# Calculate width
WIN_WIDTH = XSQUARES * SQUAREWIDTH
WIN_HEIGHT = YSQUARES * SQUAREWIDTH

# Calculate window positioning
WIN_X = (SCREEN_WIDTH / 2) - (WIN_WIDTH / 2)
WIN_Y = (SCREEN_HEIGHT / 2) - (WIN_HEIGHT / 2)


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    # Set positioning of the window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WIN_X, WIN_Y)

    # Set window dimensions
    size = [WIN_WIDTH, WIN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # Create title
    pygame.display.set_caption("Dijkstra Demonstration")

    # Create objects
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = gui.Game(screen)

    # Main game loop
    while not done:
        # Process events
        done = game.process_events()

        # Draw the current frame
        game.display_frame()

        # Pause for the next frame
        clock.tick(30)
    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
