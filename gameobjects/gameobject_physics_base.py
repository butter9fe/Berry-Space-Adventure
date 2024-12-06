from gameobjects.gameobject_base import *
from constants import *

class GameObject_Physics_Base(GameObject_Base):
    def __init__(self, go_type: GameObjectType, canvas: tk.Canvas, position: Vector2 = Vector2(), size: Vector2 = Vector2(25, 25), mass: float = 1.0):
        super().__init__(go_type, canvas, position, size)

        self.mass = mass
        self.velocity = Vector2()
        self.normal = Vector2()

    def update(self, time_scale):
        self.velocity += Vector2(0,  GRAVITY * self.mass * time_scale) # Apply constant gravity
        self.update_pos(self.position + self.velocity * time_scale)

    """
    2D Elastic Collision
    Reference (psuedocode): https://stackoverflow.com/questions/54483073/simple-way-to-resolve-2d-elastic-collision-between-circles
    """
    def elastic_collision(self, other: GameObject_Base):
        deltaPos = self.position - other.position

        # If other object is a Physics object, we want to apply velocity to both objects
        if isinstance(other, GameObject_Physics_Base):
            other = GameObject_Physics_Base(other)
            direction = deltaPos * ((self.velocity - other.velocity).dot(deltaPos) / deltaPos.length_squared())
            direction = direction.normalized() # Normalized to 0-1 scale so that distance does not matter

            self.velocity = -self.velocity.absolute_vector() * direction # Bounce in reversed direction by the magnitude of the current velocity
            other.velocity = -other.velocity.absolute_vector() * direction # Bounce in reversed direction by the magnitude of the current velocity

        # If other object is just a static gameobject, just apply velocity to one object
        else:
            deltaPos = self.position - other.position
            direction = deltaPos * (self.velocity.dot(deltaPos) / deltaPos.length_squared())
            direction = direction.normalized() # Normalized to 0-1 scale so that distance does not matter
            self.velocity = -self.velocity.absolute_vector() * direction # Bounce in reversed direction by the magnitude of the current velocity

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
    def collision_response(self, other: GameObject_Base):
        raise NotImplementedError(f"{self.__class__.__name__} does not implement check_collision()!") 
    # endregion