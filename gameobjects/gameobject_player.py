import tkinter as tk
import math as m

from utils.vector2 import Vector2
from gameobjects.gameobject_physics_base import * 
from utils.audioplayer import SoundManager
from utils.soundthreadmanager import sound_thread
from utils.math_extensions import *
from screens.dialogue_win import Dialogue_Win
from screens.dialogue_lose import Dialogue_Lose
from screens.dialogue_1 import Dialogue

class Player(GameObject_Physics_Base):
    # Constants
    PLAYER_SIZE = 50

    def __init__(self, canvas: tk.Canvas, spawn_x: int, spawn_y: int, list_images: list[tk.PhotoImage]):
        self.energy =100.0
        self.health = 3
        self.list_images = list_images
        super().__init__(GameObjectType.PLAYER, canvas, Vector2(spawn_x, spawn_y), Vector2(Player.PLAYER_SIZE, Player.PLAYER_SIZE))

        self.has_end_game = False

    def draw(self) -> int:
        image_pos = self.position - self.size
        self.berry_img = tk.PhotoImage(file='./assets/Game_Jam_Berry.png')
        self.berry_img = self.scale_image(self.berry_img, self.size.x * 2)
        self.berry_bubble_img = tk.PhotoImage(file='./assets/Game_Jam_BerryBubble.png')
        self.berry_bubble_img = self.scale_image(self.berry_bubble_img, self.size.x * 2)
        self.list_images.append(self.berry_img)
        self.list_images.append(self.berry_bubble_img)

        return self.canvas.create_image(image_pos.x, image_pos.y, image=self.berry_img, anchor='nw')
    
    def wall_collision_response(self, other: GameObject_Base):
        # Obtain opposite direction of player's current velocity to wall's normal
        direction = (self.velocity - other.normal).normalized()
        bounce_velocity =  -self.velocity.absolute_vector() * direction

        # Ensure that we always bounce the player in the direction of the wall
        # This prevents the player from being stuck in the wall
        if other.normal.x != 0:
            bounce_velocity.x = m.copysign(bounce_velocity.x, other.normal.x)
        if other.normal.y != 0:
            bounce_velocity.y = m.copysign(bounce_velocity.y, other.normal.y)

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
            
            # Spike!
            case GameObjectType.SPIKE:
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

            case GameObjectType.SPIKE:
                sound_thread.play_sfx("./assets/sounds/sfx/item_-hp.wav")
                self.elastic_collision(other) # Collision response
                self.canvas.delete(other.canvas_object) # Remove spike
                other.canvas_object = None
                self.damage_hp(HEALTH_LOSE_FROM_SPIKE) # Decrease hp!

            case GameObjectType.WALL:
                self.wall_collision_response(other)

                # Minimum velocity to bounce back in case we get stuck
                if (other.normal.x == 1):
                    self.velocity.x = max(self.velocity.x, 5)
                elif (other.normal.x == -1):
                    self.velocity.x = min(self.velocity.x, -5)


            case GameObjectType.SPACESHIP:
                if other.is_active: # Start ship, acts as a "wall"
                    #sound_thread.play_sfx("./assets/sounds/sfx/item_spaceship.wav")
                    self.wall_collision_response(other)
                    self.velocity.y = min(self.velocity.y, -0.5) # Don't allow falling through the floor
                    self.modify_energy(100 - self.energy) # Set directly to 100

                else: # End ship!
                    # Reset velocity, clamping y as well
                    self.velocity.x = 0
                    self.velocity.y = -3

                    self.has_end_game = True # Set end game
                    other.is_active = True # Reenable collision for spaceship
                    other.normal = Vector2(0, -1) # Set normal to be the same as start

                    self.canvas.after(5, lambda: self.show_dialogue())

            case _:
                pass # do nothing

    def modify_energy(self, energy_to_add: float):
        self.energy = clamp(self.energy + energy_to_add, 0, 100)
        self.energy_update_callback()

    def damage_hp(self, health_to_minus: float):
        self.health = clamp(self.health - health_to_minus, 0, 3)
        self.hp_update_callback()
        if self.health == 0:
            self.has_end_game = True
            Dialogue_Lose(self.canvas)

    def show_dialogue(self):
        if self.canvas.curr_level==2:
            Dialogue_Win(self.canvas)
        else:    
            Dialogue(self.canvas)

