import tkinter as tk
from tkinter import ttk

from gameobjects.gameobject_player import Player
from ctypes import windll
from utils.vector2 import Vector2

class HUD(tk.Canvas):
    HP_SIZE = 50
    ENERGY_SIZE = 100

    def __init__(self, parent, player: Player):
        # Background image
        bg_img = tk.PhotoImage(file='./assets/BSO_Header.png')
        ratio = int(bg_img.width()/parent.winfo_screenwidth())
        bg_img.zoom(ratio, ratio)

        # Initialise canvas
        super().__init__(parent, bd=0, highlightthickness=0, width=parent.winfo_screenwidth(), height=bg_img.height(), bg='black')

        # Initialise variables
        global hud_images
        hud_images = [] # List of PhotoImages used by HUD
        self.health = [] # List of hp images

        # Background image
        hud_images.append(bg_img) # store in global variable so GC doesn't delete our image
        self.create_image(0, 0, image=bg_img, anchor='nw')

        # Hearts
        for i in range(3):
            # Create image at desired size
            hp_img = tk.PhotoImage(file='./assets/BSO_MG_PinkHeart.png')
            scale = int(hp_img.height()/HUD.HP_SIZE)
            hp_img = hp_img.subsample(scale, scale) # Scale HP to correct size
            hud_images.append(hp_img) # store in global variable so GC doesn't delete our images

            # Create image, starting from 50 pixels from the left and 20 pixels from the top, separating each heart by 1.25x the width of one heart
            hp_image = self.create_image(50 + i * hp_img.width() * 1.25, 20, image=hp_img, anchor='nw')

            # Append to list
            self.health.append(hp_image)
        player.hp_update_callback = lambda: self.on_health_update(player)

        # Energy
        # Frame
        energy_frame_img = tk.PhotoImage(file='./assets/BSO_UI_Energy.png')
        scale = int(energy_frame_img.height()/HUD.ENERGY_SIZE)
        top_left_x = parent.winfo_screenwidth() * 0.5 - energy_frame_img.width() * 0.5
        
        # Fill
        fill_padding = Vector2(35, 30)
        self.energy_top_left = Vector2(top_left_x, 5) + fill_padding
        self.energy_bot_right = Vector2(top_left_x + energy_frame_img.width(), energy_frame_img.height() + 1) - fill_padding
        self.energy = self.create_rectangle(self.energy_top_left.x, self.energy_top_left.y, self.energy_bot_right.x, self.energy_bot_right.y, fill='#B8FFF1', outline='#B8FFF1')
        player.energy_update_callback = lambda: self.on_energy_update(player)

        energy_frame_img = energy_frame_img.subsample(scale, scale) # Scale Energy to correct size
        hud_images.append(energy_frame_img) # store in global variable so GC doesn't delete our images
        self.create_image(top_left_x, 0, image=energy_frame_img, anchor='nw')

        self.pack()

    def on_health_update(self, player: Player):
        for i in range(len(self.health)):
            if i < player.health:
                self.itemconfig(self.health[i], state='normal')
            else:
                self.itemconfig(self.health[i], state='hidden')

    def on_energy_update(self, player: Player):
        energy_width = self.energy_bot_right.x - self.energy_top_left.x
        energy_ratio = player.energy / 100.0
        new_right_x = self.energy_top_left.x + energy_width * energy_ratio
        self.coords(self.energy, self.energy_top_left.x, self.energy_top_left.y, new_right_x, self.energy_bot_right.y)