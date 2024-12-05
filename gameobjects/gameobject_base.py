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
    def __init__(self, go_type: GameObjectType, canvas: tk.Canvas, position = Vector2()):
        self.go_type = go_type
        self.position = position

        self.canvas = canvas
        self.canvas_object = self.draw()

    def update_pos(self, new_pos: Vector2):
        # Clamp position to canvas bounds
        self.canvas.update_idletasks() # Calls all pending idle tasks to ensure we get an accurate canvas size
        canvas_size = Vector2(self.canvas.winfo_width(), self.canvas.winfo_height()) * CANVAS_MULTIPLIER # store maximum bounds of the canvas
        new_pos = mx.clamp(new_pos, Vector2(0, 0), canvas_size)
        
        # Update position
        delta_pos = new_pos - self.position # store change in position
        self.canvas.move(self.canvas_object, delta_pos.x, delta_pos.y) # move based on delta
        self.position = new_pos # update variable

    ###
    ### Functions to implement in subclasses
    ###
    """
    Draw the object on the canvas
    """
    def draw(self) -> int:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement draw()!")
        

