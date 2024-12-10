import tkinter as tk
import random as r

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Spike(GameObject_Base):
    # Constants
    SPIKE_SIZE = 35

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int, list_images: list[tk.PhotoImage]):
        self.list_images = list_images
        
        #Set max random Value
        if spawn_x <= (0.5* canvas.winfo_width()):
            spawn_x1=0.5*canvas.winfo_width()-spawn_x
        else :
            spawn_x1=spawn_x-0.5*canvas.winfo_width()

        self.max_float_offset = r.uniform(10, spawn_x1) #r.uniform(lower rad limit, upper rad limit)
        self.float_dir = r.randint(0, 1) * 2 - 1 # -1 or 1
        self.float_offset = self.float_dir * self.max_float_offset 
        super().__init__(GameObjectType.SPIKE, canvas, Vector2(spawn_x, spawn_y), Vector2(Spike.SPIKE_SIZE, Spike.SPIKE_SIZE))

    def draw(self) -> int:
        image_pos = self.position - self.size

        spike_img = tk.PhotoImage(file='./assets/spike.png')
        spike_img = self.scale_image(spike_img, self.size.x * 2)
        self.list_images.append(spike_img)

        return self.canvas.create_image(image_pos.x, image_pos.y, image=spike_img, anchor='nw')
    
    def update(self, time_scale):
        # Float up and down
        delta_x =  SPIKE_FLOAT_SPEED * self.float_dir * time_scale
        self.float_offset += delta_x
        if (self.float_dir == 1 and self.float_offset > self.max_float_offset) or (self.float_dir == -1 and self.float_offset < -self.max_float_offset):
            self.float_dir *= -1 # flip directions

        # Update position based on float
        self.canvas.move(self.canvas_object, delta_x, 0) # move based on delta
        self.position.x += delta_x # update variable

        # Despawn when far out of camera ranges
        coords = self.canvas.coords(self.canvas_object)
        canvasStart = self.canvas.canvasy(0)
        canvasEnd = canvasStart + self.canvas.winfo_height()
        tolerance = OFFSCREEN_SPAWN_MULTIPLIER * self.canvas.winfo_height() # Keep stars still that are half a screen away from player

        if coords[1] < canvasStart - tolerance or coords[1] > canvasEnd + tolerance:
            self.canvas.delete(self.canvas_object)
            self.canvas_object = None
