### Imports
# Modules
import tkinter as tk
import random as r

# Classes
from gameobjects.gameobject_player import Player
from utils.timer import Timer
from utils.vector2 import Vector2
from constants import *

class Game(tk.Canvas):
    def __init__(self, parent):
        global bg_img # Needed beause tkinter is funky and needs the image to be in same scope as mainloop

        # Initialise variables
        screen_size = Vector2(parent.winfo_screenwidth(), parent.winfo_screenheight()) # Obtain size of root window
        self.canvas_size = screen_size * CANVAS_MULTIPLIER # Actual size of canvas is much larger than the screen size to allow for scrolling
        self.center_offset = screen_size/self.canvas_size * 0.5 # By default, coordinate system is top left. As such, we want to always apply the same offset to canvas movement such that it is centered instead
        self.mouse_down = False # Flag to check if mouse is pressed
        self.game_objects = []

        # Initialise canvas
        super().__init__(parent, background='black', bd=0, highlightthickness=0, scrollregion=(0, 0, self.canvas_size.x, self.canvas_size.y))
        self.pack(expand = True, fill = 'both')

        # Add space background
        # TODO: Placeholder for now, replace with parallax effect that looks nicer if have time
        bg_img = tk.PhotoImage(file='./assets/spaceBG.png')
        self.bg = self.create_image(0, 0, image=bg_img, anchor='nw')

        # Create path from player to mouse, initialised to 0 first
        self.path = self.create_line(0, 0, 0, 0, fill="white", width=5)

        # Create player
        self.player = Player(self, self.canvas_size.x * 0.5, self.canvas_size.y * 0.9)

        # Test circles
        for _ in range(100):
            pos = self.get_random_pos(Vector2(0, 0), self.canvas_size, Vector2(1, 1))
            self.create_oval(pos.x - 10, pos.y - 10, pos.x + 10, pos.y + 10, fill='white')

        # Begin update loop
        # Only after all objects have been created
        self.timer = Timer()
        self.timer.update_timer(parent, self.update)

        # Event bindings
        self.bind('<ButtonPress-1>', self.on_mouse_down)
        self.bind('<ButtonRelease-1>', self.on_mouse_up)

    def update(self, time_scale):     
        # Update gameobjects
        self.player.update(time_scale)

        # Move canvas 'camera' to center on player's current position
        center_coords = self.player.position / self.canvas_size - self.center_offset
        self.xview_moveto(center_coords.x)
        self.yview_moveto(center_coords.y)

        # Attach background to canvas camera to keep it stationary
        # Get coordinates of background currently
        x, y = self.coords(self.bg)
        # Get displacements from current top left of canvas position
        dx = self.canvasx(0) - x
        dy = self.canvasy(0) - y
        # Move background back to center of canvas
        self.move(self.bg, dx, dy)

        # Update path if mouse is down
        if self.mouse_down:
            absolute_mouse_pos = self.relative_to_absolute(Vector2(self.winfo_pointerx() - self.winfo_rootx(), self.winfo_pointery() - self.winfo_rooty()))
            self.coords(self.path, self.player.position.x, self.player.position.y, absolute_mouse_pos.x, absolute_mouse_pos.y)

    # region Events
    def on_mouse_down(self, event):
        # Set flag
        self.mouse_down = True
        # Begin slow-mo
        self.timer.update_timescale(0.5)

    def on_mouse_up(self, event):
        # Set flag
        self.mouse_down = False
        # End slow-mo
        self.timer.update_timescale(1.0)

        # Shoot the player!
        absolute_mouse_pos = self.relative_to_absolute(Vector2(event.x, event.y)) # event provides us with position relative to widget position, but we want the world coordinates
        print(absolute_mouse_pos.x, absolute_mouse_pos.y, self.player.position.x, self.player.position.y)
        self.player.velocity = (self.player.position - absolute_mouse_pos) * PLAYER_SHOOT_STRENGTH

        # Hide path
        self.coords(self.path, 0, 0, 0, 0)

    def on_click(self, event):
        print("Click")
    # endregion

    # region Utility Functions
    """
    Helper function to convert relative coordinates (ie 0,0 top left, canvas_size bot right) to absolute coordinates based on scrolling position
    """
    def relative_to_absolute(self, relative_coords: Vector2) -> Vector2:
        return relative_coords + Vector2(self.canvasx(0), self.canvasy(0))
    
    def get_random_pos(self, min_pos: Vector2, max_pos: Vector2, scale: Vector2) -> Vector2:
        return Vector2(r.randrange(min_pos.x, max_pos.x), r.randrange(min_pos.y, max_pos.y))
    # endregion