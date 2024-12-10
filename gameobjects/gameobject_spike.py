import tkinter as tk

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Spike(GameObject_Base):
    # Constants
    SPIKE_SIZE = 35

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int, list_images: list[tk.PhotoImage]):
        self.list_images = list_images
        super().__init__(GameObjectType.SPIKE, canvas, Vector2(spawn_x, spawn_y), Vector2(Spike.SPIKE_SIZE, Spike.SPIKE_SIZE))

    def draw(self) -> int:
        image_pos = self.position - self.size

        spike_img = tk.PhotoImage(file='./assets/spike.png')
        spike_img = self.scale_image(spike_img, self.size.x * 2)
        self.list_images.append(spike_img)

        return self.canvas.create_image(image_pos.x, image_pos.y, image=spike_img, anchor='nw')
    
    def update(self, time_scale):
        # Despawn when far out of camera range
        coords = self.canvas.coords(self.canvas_object)
        canvasStart = self.canvas.canvasy(0)
        canvasEnd = canvasStart + self.canvas.winfo_height()
        tolerance = OFFSCREEN_SPAWN_MULTIPLIER * self.canvas.winfo_height() # Keep Spike still that are half a screen away from player
        
        if coords[1] < canvasStart - tolerance or coords[1] > canvasEnd + tolerance:
            self.canvas.delete(self.canvas_object)
            self.canvas_object = None
