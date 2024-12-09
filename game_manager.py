### Imports
# Modules
import tkinter as tk
from tkinter import ttk
# Classes
from screens.screen_game import Game
from screens.main_menu import launch_sequence
from utils.audioplayer import SoundManager
from utils.soundthreadmanager import sound_thread

class GameManager(object):
    def __new__(cls): # Singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # Initialise sound manager -SK
        global sound_manager
        #sound_manager = SoundManager()
        #sound_manager.start()
        sound_thread = SoundManager.get_sound_player_thread()
        self.curr_level = 0

        # Setting up the window
        self.root = tk.Tk() # Create a window
        self.root.title("Berry's Starlight Odyssey!") # Title of application
        self.root.iconbitmap('./assets/favicon.ico') # Set icon of application
        self.root.resizable(False, False) # Prevent window from being resized
        self.root.state('zoomed') # Maximize window
        self.root.configure(bg='black') # Set bg to black

        # Set up screens
        self.next_level()
        self.root.mainloop() # run

    def next_level(self):
        self.curr_level += 1

        # Launch new scene
        match self.curr_level:
            case 2:
                Game(self.root, self.curr_level, self.next_level, './assets/spaceBG_2.png')
                sound_thread.play_bgm("./assets/sounds/bgm/game_space_lv2.wav") #Lv2 Music

            case _: # Default/Level 1
                Game(self.root, self.curr_level, self.next_level)
                sound_thread.play_bgm("./assets/sounds/bgm/game_space_lv1.wav") #Lv1 Music