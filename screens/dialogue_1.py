### Imports
# Modules
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.soundthreadmanager import sound_thread

# Tbh idk how u wanna do this this is just placeholder feel free to refactor this or even delete this file lol
# Call for this is under gameobject_player.py, under collision_response() and spaceship

# You can check for self.game.curr_level to display different dialogues based on what level you are on
class Dialogue:
    def __init__(self, game):
       self.game = game

       self.root = tk.Toplevel()
       self.root.geometry('400x300')
       # Make window stay on top
       self.root.attributes('-topmost', True)
       
       ttk.Button(self.root, text="Next Level", command=self.go_next_level).pack()

    def go_next_level(self):
        self.game.load_next_level() # Load next level
        self.root.destroy() # Close window