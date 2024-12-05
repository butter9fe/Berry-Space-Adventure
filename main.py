### Imports
# Modules
import tkinter as tk
from tkinter import ttk
# Classes
from screens.screen_game import Game

# Main Loop. See https://www.geeksforgeeks.org/python-main-function/
def main():
    # Setting up the window
    root = tk.Tk() # Create a window
    root.title("Berry's Space Adventure!") # Title of application
    root.iconbitmap('./assets/favicon.ico') # Set icon of application
    root.resizable(False, False) # Prevent window from being resized
    root.state('zoomed') # Maximize window

    # Set up screens
    screen_game = Game(root)
    
    root.mainloop() # run

# Start loop only if this file is ran directly
if __name__ == '__main__':
    main()