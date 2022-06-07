from abc import ABC, abstractmethod
from globalResources import Point

###########################################
###############  NAVIGATOR  ###############
###########################################
class Navigator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.velocity = Point(0, 0)
        self.direction = 0
        
    """
    MOVE
    Given a starting point,
    returns the point where the object will be at its current velocity
    """
    @abstractmethod
    def move(self, startPoint):
        return Point(0, 0)
    
    
    
############################################
###############  PLAYER NAV  ###############
############################################
class PlayerNav(Navigator):
    def __init__(self) -> None:
        super().__init__()
        self.tireAngle = 0
        
    """
    MOVE
    Given a starting point,
    returns the point where the object will be at its current velocity
    """
    def move(self, startPoint):
        endPoint = Point(0, 0)
        
        return endPoint
    
    """
    TURN
    Turns the wheels of the Vehicle, or the Vehicle itself (depending on implementation)
    """
    def turn(self, direction):
        return None

    """
    ACCELERATE
    Accelerates Vehicle in direction of movement
    """
    def accelerate(self, direction):
        return None
    
    
    
############################################
###############  MOTIONLESS  ###############
############################################
class Motionless(Navigator):
    def __init__(self) -> None:
        super().__init__()
        
    """
    MOVE
    Given a starting point,
    returns the point where the object will be at its current velocity
    """
    def move(self, startPoint):
        return startPoint
    
    
    
###############################################
###############  WARP WHEN HIT  ###############
###############################################
class WarpWhenHit(Navigator):
    def __init__(self) -> None:
        super().__init__()
        warpPointOptions = []
        
    """
    MOVE
    Chooses a warp point from among the internal list of options
    that is different than the position given
    """
    def move(self, startPoint):
        endPoint = Point(0, 0)
        
        return endPoint
    
    
    
#####################################################
###############  WARP WHEN HIT TIMED  ###############
#####################################################
class WarpWhenHitTimed(WarpWhenHit):
    def __init__(self) -> None:
        super().__init__()
        warpPointOptions = []
        
    """
    MOVE
    Chooses a warp point from among the internal list of options
    that is different than the position given
    """
    def move(self, startPoint):
        return super().move()
    
    
    
################################################
###############  CYCLE WHEN HIT  ###############
################################################
class CycleWhenHit(Navigator):
    def __init__(self) -> None:
        super().__init__()
        targetPositions = []
        currentIndex = 0
        
    """
    MOVE
    Cycles the currentIndex to the next position in the list,
    restarting at 0 when the end of the list is reached.
    """
    def move(self, startPoint):
        endPoint = Point(0, 0)
        
        return endPoint