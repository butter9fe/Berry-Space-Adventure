import tkinter as tk
import math as m

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 
from utils.audioplayer import SoundManager
from utils.soundthreadmanager import sound_thread
from utils.math_extensions import *

class Player(GameObject_Physics_Base):
    # Constants
    PLAYER_SIZE = 25

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int):
        super().__init__(GameObjectType.PLAYER, canvas, Vector2(spawn_x, spawn_y), Vector2(Player.PLAYER_SIZE, Player.PLAYER_SIZE))
        self.energy = tk.DoubleVar(value=100)
        self.health = tk.IntVar(value=3)

    def draw(self) -> int:
        top_left = self.position - self.size
        bot_right = self.position + self.size
        return self.canvas.create_oval(top_left.x, top_left.y, bot_right.x, bot_right.y, fill='yellow', outline='white')
    
    def wall_collision_response(self, other: GameObject_Base):
        # Obtain opposite direction of player's current velocity to wall's normal
        direction = (self.velocity - other.normal).normalized()

        # Ensure that we always bounce the player in the direction of the wall
        # This prevents the player from being stuck in the wall
        if other.normal.x != 0:
            direction.x = m.copysign(direction.x, other.normal.x)
        if other.normal.y != 0:
            direction.y = m.copysign(direction.y, -other.normal.y)

        bounce_velocity =  -self.velocity.absolute_vector() * direction

        # Limit bounce velocity so you don't bounce back all the way
        bounce_velocity.x = clamp(bounce_velocity.x, -8, 8)
        bounce_velocity.y = max(bounce_velocity.y, -5)

        # Diminish velocity as well
        self.velocity = bounce_velocity * 0.8
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
                return dis_diff.length_squared() <= (self.size.x + other.size.x) * (self.size.y + other.size.y)
            
            # Walls/Spaceship
            case GameObjectType.WALL:
                dis_diff = abs(other.position.x - self.position.x) # We don't care about y
                return dis_diff <= self.size.x + other.size.x
            
            case GameObjectType.SPACESHIP:
                projected_dist = (self.position - other.position).dot(other.normal)
                return projected_dist < 0
                
            
            case _: # If nothing matches, no collision!
                return False
    
    '''
    After a collision has occured, this function is called to resolve the collision
    Basically, all the logic pertaining to what happens after a collision (gain score, velocity change, gain/lose hp, powerups, etc.) resides here!
    '''
    def collision_response(self, other: GameObject_Base):
        match other.go_type:
            case GameObjectType.STAR:
                sound_thread.play_sfx("./assets/sounds/sfx/item_star.wav")
                self.elastic_collision(other) # Collision response
                self.canvas.delete(other.canvas_object) # Remove star
                other.canvas_object = None
                self.modify_energy(ENERGY_GAIN_FROM_STAR) # Increase energy!

            case GameObjectType.WALL:
                self.wall_collision_response(other)

            case GameObjectType.SPACESHIP:
                sound_thread.play_sfx("./assets/sounds/sfx/item_spaceship.wav")
                self.wall_collision_response(other)
                self.modify_energy(100 - self.energy.get()) # Set directly to 100

            case _:
                pass # do nothing

    def modify_energy(self, energy_to_add: float):
        self.energy.set(clamp(self.energy.get() + energy_to_add, 0, 100))

