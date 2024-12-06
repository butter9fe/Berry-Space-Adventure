import tkinter as tk

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 
from utils.audioplayer import SoundManager
from utils.soundthreadmanager import sound_thread

class Player(GameObject_Physics_Base):
    # Constants
    PLAYER_SIZE = 25

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int):
        super().__init__(GameObjectType.PLAYER, canvas, Vector2(spawn_x, spawn_y), Vector2(Player.PLAYER_SIZE, Player.PLAYER_SIZE))

    def draw(self) -> int:
        top_left = self.position - self.size
        bot_right = self.position + self.size
        return self.canvas.create_oval(top_left.x, top_left.y, bot_right.x, bot_right.y, fill='yellow', outline='white')
    
    '''
    Checks if a collision has occured between this object and another object
    Returns a boolean if this is True or False
    '''
    def check_collision(self, other: GameObject_Base) -> bool:
        match other.go_type: # Switch case based on other object's type
            # Star!
            case GameObjectType.STAR:
                dis_diff = other.position - self.position

                # Perpendicular! Always return false 
                if self.velocity.dot(dis_diff) <= 0:
                    return False

                # Else just check if the distance is less than the sum of the size of the two objects
                return dis_diff.length_squared() <= (self.size.x+ other.size.x) * (self.size.y + other.size.y)
            
            case _: # If nothing matches, no collision!
                return False
    
    '''
    After a collision has occured, this function is called to resolve the collision
    Basically, all the logic pertaining to what happens after a collision (gain score, velocity change, gain/lose hp, powerups, etc.) resides here!
    '''
    def collision_response(self, other: GameObject_Base):
        match other.go_type:
            case GameObjectType.STAR:
                sound_thread.play_sfx("./assets/sounds/sample_collected_star.wav")
                self.elastic_collision(other)
                self.canvas.delete(other.canvas_object) # Remove star
                other.canvas_object = None
                # Increase energy!

            case _:
                pass # do nothing

