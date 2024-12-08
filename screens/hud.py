import tkinter as tk
from tkinter import ttk

from gameobjects.gameobject_player import Player

class HUD(tk.Frame):
    def __init__(self, parent, player: Player):
        super().__init__(parent)
        
        energy = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate', variable=player.energy, maximum=100)
        energy.pack()