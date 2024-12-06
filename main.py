### Imports
# Modules
import tkinter as tk
from tkinter import ttk
# Classes
from screens.screen_game import Game
from utils.audioplayer import SoundManager
from utils.soundthreadmanager import sound_thread

# Main Loop. See https://www.geeksforgeeks.org/python-main-function/
def main():

    # Initialise sound manager -SK
    global sound_manager
    sound_manager = SoundManager()
    sound_manager.start()

    # Setting up the window
    root = tk.Tk() # Create a window
    root.title("Berry's Starlight Odyssey!") # Title of application
    root.iconbitmap('./assets/favicon.ico') # Set icon of application
    root.resizable(False, False) # Prevent window from being resized
    root.state('zoomed') # Maximize window

    # Play background music (BGM)
    sound_thread.play_bgm("./assets/sounds/space_lv1.wav")

    # Set up screens
    screen_game = Game(root)
    root.mainloop() # run

# Start loop only if this file is ran directly
if __name__ == '__main__':
    main()
