from abc import ABC, abstractmethod
from simEnvironment.globalResources import Point
from simEnvironment.hurtbox import Circle, Rect
from simEnvironment.image import Sprite, RectShape, TargetShape
from simEnvironment.navigator import PlayerNav, Motionless, WarpWhenHit, WarpWhenHitTimed, CycleWhenHit

############################################
###############  COLLIDABLE  ###############
############################################
class Collidable(ABC):
    def __init__(self) -> None:
        super().__init__()
        position = Point(0, 0)
        rotation = 0
        hurtbox = Rect()
        nav = Motionless()
        img = RectShape(0, 0)

    """
    ON COLLISION
    The Collidable object can determine what happens when a collision occurs
    """
    @abstractmethod
    def onCollision(self):
        return None
    
    """
    CHECK COLLISION WITH
    Determines if the two hurtboxes have collided,
    and calls onCollision() for each Collidable if that is the case
    """
    def checkCollisionWith(self, otherCollidable):
        return None
    
    """
    MOVE
    Calls nav's move function
    """
    def move(self):
        return None
    
    """
    DRAW
    Calls img's draw function
    """
    def draw(self):
        return None

        
        
#########################################
###############  VEHICLE  ###############
#########################################
class Vehicle(Collidable):
    def __init__(self) -> None:
        super().__init__()
        self.hurtbox = Rect()
        self.nav = PlayerNav()
        self.alive = True

    """
    ON COLLISION
    Changes Vehicle status to not alive
    """
    def onCollision(self):
        return super().onCollision()
    


########################################
###############  TARGET  ###############
########################################
class Target(Collidable):
    def __init__(self, locations) -> None:
        super().__init__()
        self.hurtbox = Circle()
        self.nav = WarpWhenHit(locations)

    """
    ON COLLISION
    Initiates process of moving target to next position
    """
    def onCollision(self):
        return super().onCollision()
    
    
    
######################################
###############  WALL  ###############
######################################
class Wall(Collidable):
    def __init__(self) -> None:
        super().__init__()  # No changes needed from original values
        self.width = 0
        self.height = 0
        
    """
    ON COLLISION
    No activity from the Wall
    """
    def onCollision(self):
        return super().onCollision()