from enum import Enum
import tkinter as tk

from utils.vector2 import Vector2
import utils.math_extensions as mx
from  constants import *

class GameObjectType(Enum):
    NONE = 0,
    PLAYER = 1,
    STAR = 2,
    WALL = 3,
    SPIKE = 4

class GameObject_Base():
    def __init__(self, go_type: GameObjectType, canvas: tk.Canvas, position = Vector2(), size = Vector2(25, 25)):
        self.go_type = go_type
        self.position = position
        self.size = size

        self.canvas = canvas
        self.canvas_object = self.draw()

    def update(self, time_scale):
        pass

    def update_pos(self, new_pos: Vector2):
        # Clamp position to canvas bounds
        self.canvas.update_idletasks() # Calls all pending idle tasks to ensure we get an accurate canvas size
        canvas_size = Vector2(self.canvas.winfo_width(), self.canvas.winfo_height() * CANVAS_MULTIPLIER) # store maximum bounds of the canvas
        #new_pos = mx.clamp(new_pos, Vector2(0, 0), canvas_size) # TODO
        
        # Update position
        delta_pos = new_pos - self.position # store change in position
        self.canvas.move(self.canvas_object, delta_pos.x, delta_pos.y) # move based on delta
        self.position = new_pos # update variable

    """
    Utility function to size up/down image to desired size, used for draw function.
    We only scale based on width to maintain the original image ratio
    """
    def scale_image(self, image: tk.PhotoImage, size_x: int) -> tk.PhotoImage:
        scale = size_x / image.width()
        if scale < 1: # scale down
            scale = int(1/scale) # convert to how much to scale down (ie 0.5 -> scale down by 2x)
            return image.subsample(scale, scale) # scale down image and set as new image
        else: # size up
            scale = int(scale)
            return image.zoom(scale, scale)

    ###
    ### Functions to implement in subclasses
    ###
    """
    Draw the object on the canvas
    """
    def draw(self) -> int:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement draw()!")
        

