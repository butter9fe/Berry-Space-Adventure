import tkinter as tk

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Star(GameObject_Base):
    # Constants
    STAR_RADIUS = 5

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int):
        super().__init__(GameObjectType.STAR, canvas, Vector2(spawn_x, spawn_y))

    def draw(self) -> int:
        top_left = self.position - Star.STAR_RADIUS
        bot_right = self.position + Star.STAR_RADIUS
        return self.canvas.create_oval(top_left.x, top_left.y, bot_right.x, bot_right.y, fill='yellow', outline='black')

