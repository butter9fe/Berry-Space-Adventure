import tkinter as tk

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Spaceship(GameObject_Base):
    # Constants
    SHIP_HEIGHT = 100

    def __init__(self, canvas: tk.Canvas, spawn_y: int, is_start: bool, list_images: list[tk.PhotoImage]):
        self.is_start = is_start # Whether it's the starting spaceship or end
        self.is_active = is_start # Whether collision is active
        self.normal = Vector2(0, -1 if is_start else 1)
        self.list_images = list_images

        canvas.update_idletasks()
        super().__init__(GameObjectType.SPACESHIP, canvas, Vector2(canvas.winfo_width() * 0.5, spawn_y - Spaceship.SHIP_HEIGHT), Vector2(canvas.winfo_width() * 0.5, Spaceship.SHIP_HEIGHT))

    def draw(self) -> int:
        ship_img = tk.PhotoImage(file='./assets/sprite_ship.png')
        ship_img = self.scale_image(ship_img, self.size.y * 2, False)
        self.list_images.append(ship_img)

        image_pos = self.position - Vector2(ship_img.width(), ship_img.height()) * 0.5
        return self.canvas.create_image(image_pos.x, image_pos.y, image=ship_img, anchor='nw')
