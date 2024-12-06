### Imports
# Modules
import tkinter as tk
import random as r

# Classes
from gameobjects.gameobject_base import GameObject_Base
from gameobjects.gameobject_player import Player
from gameobjects.gameobject_star import Star
from utils.timer import Timer
from utils.vector2 import Vector2
from constants import *

class Game(tk.Canvas):
    def __init__(self, parent):
        global bg_img # Required so GC doesn't delete the image due to no references

        # Initialise variables
        screen_size = Vector2(parent.winfo_screenwidth(), parent.winfo_screenheight()) # Obtain size of root window
        self.canvas_size = Vector2(screen_size.x, screen_size.y * CANVAS_MULTIPLIER) # Actual size of canvas is much larger than the screen size to allow for scrolling
        self.center_offset = screen_size/self.canvas_size * 0.5 # By default, coordinate system is top left. As such, we want to always apply the same offset to canvas movement such that it is centered instead
        self.mouse_down = False # Flag to check if mouse is pressed
        self.game_objects : list[GameObject_Base] = [] # List of game objects
        self.active_star_count = 0

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

        # Create stars
        global star_images # Required so GC doesn't delete the images due to no references
        star_images = []
        self.spawn_stars()

        # Begin update loop
        # Only after all objects have been created
        self.timer = Timer()
        self.timer.update_timer(parent, self.update)

        # Event bindings
        self.bind('<ButtonPress-1>', self.on_mouse_down)
        self.bind('<ButtonRelease-1>', self.on_mouse_up)

    def update(self, time_scale):     
        # Update player
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

        for go in self.game_objects:
            # Update gameobjects
            go.update(time_scale)

            # Check for collisions with player
            if (self.player.check_collision(go)):
                self.player.collision_response(go)

            # Remove dead gameobjects
            if (go.canvas_object == None):
                self.game_objects.remove(go)
                if (isinstance(go, Star)):
                    self.active_star_count -= 1

        # Continuously spawn new stars if we go below the maximum
        self.spawn_stars()

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
    
    def get_random_pos(self, min_pos: Vector2, max_pos: Vector2) -> Vector2:
        min_pos.cast_to_int_vector()
        max_pos.cast_to_int_vector()
        return Vector2(r.randrange(min_pos.x, max_pos.x), r.randrange(min_pos.y, max_pos.y))
    
    def spawn_stars(self):
        stars_to_spawn = MAX_STARS - self.active_star_count
        if (stars_to_spawn < 1): # No stars to spawn needed! Terminate function early
            return

        # Get current window position in canvas
        window_top_pos = Vector2(0, self.canvasy(0))
        window_bot_pos = Vector2(self.canvas_size.x, self.canvasy(0) + self.winfo_height() * (1 + OFFSCREEN_SPAWN_MULTIPLIER))

        print(window_top_pos.y, window_bot_pos.y)

        for _ in range(stars_to_spawn):
            pos = self.get_random_pos(window_top_pos, window_bot_pos) # Spawn within confines of what is visible + half a screen away
            star = Star(self, pos.x, pos.y, star_images)
            self.game_objects.append(star)
            self.active_star_count += 1
    # endregion