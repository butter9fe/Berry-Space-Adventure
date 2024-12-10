import tkinter as tk
import random as r

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Star(GameObject_Base):
    # Constants
    STAR_SIZE = 25

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int, list_images: list[tk.PhotoImage]):
        self.list_images = list_images
        self.max_float_offset = r.uniform(5, 15)
        self.float_dir = r.randint(0, 1) * 2 - 1 # -1 or 1
        self.float_offset = self.float_dir * self.max_float_offset 
        super().__init__(GameObjectType.STAR, canvas, Vector2(spawn_x, spawn_y + self.float_offset), Vector2(Star.STAR_SIZE, Star.STAR_SIZE))

    def draw(self) -> int:
        image_pos = self.position - self.size

        star_img = tk.PhotoImage(file='./assets/star.png')
        star_img = self.scale_image(star_img, self.size.x * 2)
        self.list_images.append(star_img)

        return self.canvas.create_image(image_pos.x, image_pos.y, image=star_img, anchor='nw')
    
    def update(self, time_scale):
        # Float up and down
        delta_y =  STAR_FLOAT_SPEED * self.float_dir * time_scale
        self.float_offset += delta_y
        if (self.float_dir == 1 and self.float_offset > self.max_float_offset) or (self.float_dir == -1 and self.float_offset < -self.max_float_offset):
            self.float_dir *= -1 # flip directions

        # Update position based on float
        self.canvas.move(self.canvas_object, 0, delta_y) # move based on delta
        self.position.y += delta_y # update variable

        # Despawn when far out of camera range
        coords = self.canvas.coords(self.canvas_object)
        canvasStart = self.canvas.canvasy(0)
        canvasEnd = canvasStart + self.canvas.winfo_height()
        tolerance = OFFSCREEN_SPAWN_MULTIPLIER * self.canvas.winfo_height() # Keep stars still that are half a screen away from player
        
        if coords[1] < canvasStart - tolerance or coords[1] > canvasEnd + tolerance:
            self.canvas.delete(self.canvas_object)
            self.canvas_object = None
