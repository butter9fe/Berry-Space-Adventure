### Imports
# Modules
import tkinter as tk
from tkinter import ttk
# Classes
from screens.screen_game import Game
from screens.main_menu import launch_sequence
from utils.audioplayer import SoundManager
from utils.soundthreadmanager import sound_thread
from game_manager import GameManager

# Main Loop. See https://www.geeksforgeeks.org/python-main-function/
def main():
   #launch_sequence()
   GameManager()

# Start loop only if this file is ran directly
if __name__ == '__main__':
    main()
