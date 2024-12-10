### Imports
# Modules
import tkinter as tk
import random as r
import math as m

# Classes
from gameobjects.gameobject_base import GameObject_Base
from gameobjects.gameobject_player import Player
from gameobjects.gameobject_star import Star
from gameobjects.gameobject_spike import Spike
from gameobjects.gameobject_spaceship import Spaceship
from gameobjects.gameobject_wall import Wall
from screens.hud import HUD

from utils.timer import Timer
from utils.vector2 import Vector2
from constants import *
from utils.soundthreadmanager import sound_thread

class Game(tk.Canvas):
    def __init__(self, parent, curr_level, next_level_callback, bg_img_path='./assets/spaceBG.png'):
        # Global image references so GC doesn't delete them due to nothing referencing them
        global bg_img
        global go_images
        go_images = []

        # Initialise variables
        screen_size = Vector2(parent.winfo_screenwidth(), parent.winfo_screenheight()) # Obtain size of root window
        self.canvas_size = Vector2(screen_size.x, screen_size.y * CANVAS_MULTIPLIER) # Actual size of canvas is much larger than the screen size to allow for scrolling
        self.center_offset = screen_size/self.canvas_size * 0.5 # By default, coordinate system is top left. As such, we want to always apply the same offset to canvas movement such that it is centered instead
        self.mouse_down = False # Flag to check if mouse is pressed
        self.game_objects : list[GameObject_Base] = [] # List of game objects
        self.active_star_count = 0
        self.active_spike_count = 0
        self.curr_level = curr_level # Current level integer, used to do conditional stuff, can check for dialogues here
        self.next_level_callback = next_level_callback # Callback for going next level
        self.parent = parent

        # Initialise canvas
        super().__init__(parent, background='black', bd=0, highlightthickness=0, scrollregion=(0, 0, self.canvas_size.x, self.canvas_size.y))
        ratio = parent.winfo_screenwidth()/1920 # Get ratio of current screen width by default size of 1920
        desired_size_y = ratio * 1080 # Get desired height proportional to width
        pady = max((parent.winfo_screenheight() - desired_size_y) * 0.5, 0) # In case we go negative, we want to set padding to 0 (should never happen but a failsafe!)
        self.pack(expand = True, fill = 'both', pady=int(pady)) # Fill parent window, but add padding top and bottom if necessary to keep aspect ratio

        # Add space background
        bg_img = tk.PhotoImage(file=bg_img_path)
        bg_img = bg_img.zoom(m.ceil(ratio), m.ceil(ratio)) # zoom only takes in ints so round up :(
        self.bg = self.create_image(0, 0, image=bg_img, anchor='nw')

        # Create boundaries
        self.game_objects.append(Wall(self, True, go_images)) # Left wall
        self.game_objects.append(Wall(self, False, go_images)) # Right wall

        # Create ships
        self.game_objects.append(Spaceship(self, self.canvas_size.y - Spaceship.SHIP_HEIGHT, True, go_images)) # Beginning ship
        self.game_objects.append(Spaceship(self, self.canvas_size.y * 0.1, False, go_images)) # End ship

        # Create path from player to mouse, initialised to 0 first
        self.path = self.create_line(0, 0, 0, 0, fill="white", width=5)

        # Create player
        self.player = Player(self, self.canvas_size.x * 0.5, self.canvas_size.y * 0.95)

        # Begin update loop
        # Only after all objects have been created
        self.timer = Timer()
        self.timer.update_timer(self, self.update)

        # Initialise hud
        self.hud = HUD(self, self.player)
        self.hud.pack()

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

                if (isinstance(go, Spike)):
                    self.active_spike_count -= 1

        # Continuously spawn new stars if we go below the maximum
        self.spawn_stars()
        if self.curr_level>=2:
            self.spawn_spike()

        if self.mouse_down:
            # Update path if mouse is down
            absolute_mouse_pos = self.relative_to_absolute(Vector2(self.winfo_pointerx() - self.winfo_rootx(), self.winfo_pointery() - self.winfo_rooty()))
            self.coords(self.path, self.player.position.x, self.player.position.y, absolute_mouse_pos.x, absolute_mouse_pos.y)

            # Also deplete energy
            self.player.modify_energy(-ENERGY_DEPLETION)

    def load_next_level(self):
        self.destroy()
        self.next_level_callback()

    # region Events
    def on_mouse_down(self, event):
        if self.player.has_end_game: # Reached the top! Don't allow anymore interactions
            return

        if self.player.energy.get() < ENERGY_TO_JUMP:
            sound_thread.play_sfx("./assets/sounds/sfx/launch_unable.wav") #Play sfx: Prepare to jump
            return # Don't jump

        # Set flag
        self.mouse_down = True
        # Begin slow-mo
        self.timer.update_timescale(0.5)
        #sound_thread.play_sfx("./assets/sounds/sfx/launch_prep.wav") #Play sfx: Prepare to jump

    def on_mouse_up(self, event):
        if self.mouse_down == False: # Was not preparing to jump, ie no energy
            return

        # Set flag
        self.mouse_down = False
        # End slow-mo
        self.timer.update_timescale(1.0)
        # Deplete energy
        self.player.modify_energy(-ENERGY_TO_JUMP)

        # Shoot the player!
        absolute_mouse_pos = self.relative_to_absolute(Vector2(event.x, event.y)) # event provides us with position relative to widget position, but we want the world coordinates
        self.player.velocity = (self.player.position - absolute_mouse_pos) * PLAYER_SHOOT_STRENGTH
        # Hide path
        self.coords(self.path, 0, 0, 0, 0)
        sound_thread.play_sfx("./assets/sounds/sfx/launch_able.wav") #Play sfx: Launch able

    def on_click(self, event):
        print("Click")
    # endregion

    # region Utility Functions
    """
    Helper function to convert relative coordinates (ie 0,0 top left, canvas_size bot right) to absolute coordinates based on scrolling position
    """
    def relative_to_absolute(self, relative_coords: Vector2) -> Vector2:
        return relative_coords + Vector2(self.canvasx(0), self.canvasy(0))
    
    def get_random_pos(self, min_pos: Vector2, max_pos: Vector2, size: Vector2) -> Vector2:
        # Convert positions to integers
        min_pos.cast_to_int_vector()
        max_pos.cast_to_int_vector()
        
        # Invalid range
        if (min_pos.x >= max_pos.x or min_pos.y >= max_pos.y):
            return None

        # Initialise variables
        pos = Vector2()
        valid_pos = False
        attempts = 0 # Prevent infinite loop

        # Find a valid random position
        while not valid_pos and attempts < MAX_RANDOM_ATTEMPTS:
            pos = Vector2(r.randrange(min_pos.x, max_pos.x), r.randrange(min_pos.y, max_pos.y))
            attempts += 1

            # Check for intersection with player
            player_dist_sq = self.player.position.distance_squared(pos)
            player_min_dist_sq = size + self.player.size.x + MIN_GAP_BTW_OBJS
            if (player_dist_sq < player_min_dist_sq):
                no_intersects = False
                continue # Continue with while loop and regenerate position, no need to check other objects

            # Check for intersections with other game objects
            no_intersects = True
            for go in self.game_objects:
                dist_sq = go.position.distance_squared(pos)
                min_dist_sq = size + go.size.x + MIN_GAP_BTW_OBJS
                if (dist_sq < min_dist_sq): # Intersect found!
                    no_intersects = False
                    break  # No need to continue looping through list

            # No intersects found! Break while loop
            if no_intersects:
                valid_pos = True

        return pos if valid_pos else None
    
    def spawn_stars(self):
        stars_to_spawn = MAX_STARS - self.active_star_count
        if (stars_to_spawn < 1): # No stars to spawn! Terminate function early
            return

        # Get spawn boundary for stars, by default it is the window's current place in the canvas
        spawn_top_bound = Vector2(0, self.canvasy(0))
        spawn_bot_bound = Vector2(self.canvas_size.x, self.canvasy(0) + self.winfo_height())

        # Update spawn boundary based on how player is moving
        if (self.player.velocity.y > 0.1): # Moving down
            if (spawn_bot_bound.y < self.canvas_size.y): # If window has not reached the bottom, spawn off-screen
                spawn_top_bound.y = spawn_bot_bound.y # Top boundary is bottom of window
            spawn_bot_bound.y = min(spawn_bot_bound.y + self.winfo_height() * OFFSCREEN_SPAWN_MULTIPLIER, self.canvas_size.y * 0.97) # Bottom boundary is below the window by the offscreen multiplier, capped to the canvas size

        else: # Either moving up/stationary
            if (self.player.velocity.y < -0.1 and spawn_top_bound.y > 0): # If player is moving up, and window has not reached the top, spawn off-screen
                spawn_bot_bound.y = max(spawn_top_bound.y, self.winfo_height() * 0.8) # Bottom boundary is top of window
            else:
                spawn_bot_bound.y = min(spawn_bot_bound.y, self.canvas_size.y * 0.97) # If stationary, we don't want to spawn below spaceship
            spawn_top_bound.y = max(spawn_top_bound.y - self.winfo_height() * OFFSCREEN_SPAWN_MULTIPLIER, self.winfo_height() * 0.8) # Top boundary is above the window by the offscreen multiplier, capped to 0.1x of window height

        # Spawn stars
        for _ in range(stars_to_spawn):
            pos = self.get_random_pos(spawn_top_bound, spawn_bot_bound, Star.STAR_SIZE * 2)
            if (pos == None):
                return
            star = Star(self, pos.x, pos.y, go_images)
            self.game_objects.append(star)
            self.active_star_count += 1
    # endregion

    def spawn_spike(self):
        spike_to_spawn = MAX_SPIKE - self.active_spike_count
        if (spike_to_spawn < 1): # No Spike to spawn! Terminate function early
            return

        # Get spawn boundary for stars, by default it is the window's current place in the canvas
        spawn_top_bound = Vector2(0, self.canvasy(0))
        spawn_bot_bound = Vector2(self.canvas_size.x, self.canvasy(0) + self.winfo_height())

        # Update spawn boundary based on how player is moving
        if (self.player.velocity.y > 0.1): # Moving down
            if (spawn_bot_bound.y < self.canvas_size.y): # If window has not reached the bottom, spawn off-screen
                spawn_top_bound.y = spawn_bot_bound.y # Top boundary is bottom of window
            spawn_bot_bound.y = min(spawn_bot_bound.y + self.winfo_height() * OFFSCREEN_SPAWN_MULTIPLIER, self.canvas_size.y * 0.97) # Bottom boundary is below the window by the offscreen multiplier, capped to the canvas size

        else: # Either moving up/stationary
            if (self.player.velocity.y < -0.1 and spawn_top_bound.y > 0): # If player is moving up, and window has not reached the top, spawn off-screen
                spawn_bot_bound.y = max(spawn_top_bound.y, self.winfo_height() * 0.8) # Bottom boundary is top of window
            else:
                spawn_bot_bound.y = min(spawn_bot_bound.y, self.canvas_size.y * 0.97) # If stationary, we don't want to spawn below spaceship
            spawn_top_bound.y = max(spawn_top_bound.y - self.winfo_height() * OFFSCREEN_SPAWN_MULTIPLIER, self.winfo_height() * 0.8) # Top boundary is above the window by the offscreen multiplier, capped to 0.1x of window height

        # Spawn spike
        for _ in range(spike_to_spawn):
            pos = self.get_random_pos(spawn_top_bound, spawn_bot_bound, Spike.SPIKE_SIZE * 2)
            if (pos == None):
                return
            spike = Spike(self, pos.x, pos.y, go_images)
            self.game_objects.append(spike)
            self.active_spike_count += 1
    # endregion
