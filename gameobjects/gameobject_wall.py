import tkinter as tk

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Wall(GameObject_Base):
    def __init__(self, canvas: tk.Canvas, is_left: bool, list_images: list[tk.PhotoImage]):
        self.normal = Vector2(1 if is_left else -1, 0)
        self.list_images = list_images

        canvas.update_idletasks()
        position = Vector2(0 if is_left else canvas.winfo_width(), canvas.winfo_height() * 0.5)
        super().__init__(GameObjectType.WALL, canvas, position, Vector2(10, canvas.winfo_height()))

    def draw(self) -> int:
        return self.canvas.create_line(self.position.x, 0, self.position.x, self.canvas.winfo_height(), fill='white', width=25, state='hidden')
