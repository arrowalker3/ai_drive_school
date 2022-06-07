from abc import ABC, abstractmethod
from globalResources import Point


#########################################
###############  HURTBOX  ###############
#########################################
class Hurtbox(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    """
    COLLIDED WITH POINT
    Determines if otherPoint is within this Hurtbox's bounds
    """
    @abstractmethod
    def collidedWithPoint(self, myPosition, myRotation, otherPoint):
        return False
    
    """
    CLOSEST TO POINT
    Finds the Point on this Hurtbox that is closest to the given Point
    """
    @abstractmethod
    def closestToPoint(self, myPosition, myRotation, otherPoint):
        return Point(0, 0)

    """
    DRAW
    Draws an outline of the Hurtbox (for debugging)
    """
    @abstractmethod
    def draw(self, position, rotation):
        return None
    
    
    
######################################
###############  RECT  ###############
######################################
class Rect(Hurtbox):
    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0
        
    """
    COLLIDED WITH POINT
    Determines if otherPoint is within this Hurtbox's bounds
    """
    def collidedWithPoint(self, myPosition, myRotation, otherPoint):
        collision = False

        return collision
    
    """
    CLOSEST TO POINT
    Finds the Point on this Hurtbox that is closest to the given Point
    """
    def closestToPoint(self, myPosition, myRotation, otherPoint):
        closePoint = Point(0, 0)
        
        return closePoint

    """
    DRAW
    Draws an outline of the Hurtbox (for debugging)
    """
    def draw(self, position, rotation):
        return None
    
    
    
########################################
###############  CIRCLE  ###############
########################################
class Circle(Hurtbox):
    def __init__(self) -> None:
        super().__init__()
        self.radius = 0
        
    """
    COLLIDED WITH POINT
    Determines if otherPoint is within this Hurtbox's bounds
    """
    def collidedWithPoint(self, myPosition, myRotation, otherPoint):
        collision = False

        return collision
    
    """
    CLOSEST TO POINT
    Finds the Point on this Hurtbox that is closest to the given Point
    """
    def closestToPoint(self, myPosition, myRotation, otherPoint):
        closePoint = Point(0, 0)
        
        return closePoint

    """
    DRAW
    Draws an outline of the Hurtbox (for debugging)
    """
    def draw(self, position, rotation):
        return None