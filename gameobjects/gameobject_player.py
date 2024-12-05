import tkinter as tk

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 

class Player(GameObject_Physics_Base):
    # Constants
    PLAYER_RADIUS = 25

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int):
        super().__init__(GameObjectType.PLAYER, canvas, Vector2(spawn_x, spawn_y))

    def draw(self) -> int:
        top_left = self.position - Player.PLAYER_RADIUS
        bot_right = self.position + Player.PLAYER_RADIUS
        return self.canvas.create_oval(top_left.x, top_left.y, bot_right.x, bot_right.y, fill='yellow', outline='white')
    
    '''
    Checks if a collision has occured between this object and another object
    Returns a boolean if this is True or False
    '''
    def check_collision(self, other: GameObject_Base) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement check_collision()!") 
    
    '''
    After a collision has occured, this function is called to resolve the collision
    Basically, all the logic pertaining to what happens after a collision (gain score, velocity change, gain/lose hp, powerups, etc.) resides here!
    '''
    def collision_response(self, other: GameObject_Base) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement check_collision()!") 

