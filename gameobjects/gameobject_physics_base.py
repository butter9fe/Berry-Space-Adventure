from gameobjects.gameobject_base import *
from constants import *

class GameObject_Physics_Base(GameObject_Base):
    def __init__(self, go_type: GameObjectType, canvas: tk.Canvas, position: Vector2 = Vector2(), mass: float = 1.0):
        super().__init__(go_type, canvas, position)

        self.mass = mass
        self.velocity = Vector2()
        self.normal = Vector2()

    def update(self, time_scale):
        self.velocity += Vector2(0,  GRAVITY * self.mass * time_scale) # Apply constant gravity
        self.update_pos(self.position + self.velocity * time_scale)

    ###
    # region  Functions to implement in subclasses
    ###
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
    # endregion