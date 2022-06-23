from abc import ABC, abstractmethod
import math
import pygame
import random
from simEnvironment.globalResources import Point, FORWARD, BACKWARD, LEFT, RIGHT, WIDTH_BOARD, HEIGHT_BOARD

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
    Moves the rectangle based on class distinctions
    """
    @abstractmethod
    def move(self, rect):
        pass
    
    
    
############################################
###############  PLAYER NAV  ###############
############################################
class PlayerNav(Navigator):
    def __init__(self) -> None:
        super().__init__()
        self.tireAngle = 0
        self.maxTireAngle = 45
        self.speed = 0
        self.vehicleAngle = 0
        self.turnSpeed = 10
        self.acceleration = 0.75
        self.maxSpeed = 20
        self.speedChange = False
        
    """
    MOVE
    Moves the rectangle in the stored direction and speed
    """
    def move(self, rect):
        dx = math.cos(math.radians(self.vehicleAngle)) * self.speed
        dy = math.sin(math.radians(self.vehicleAngle)) * self.speed
        
        rect.move_ip(dx, -dy)
        # self.rect.x = (self.rect.x + dx) % 200
        # self.rect.y = (self.rect.y - dy) % 200
        
        self.applyFriction()
        
    def applyFriction(self):
        # Only apply if there hasn't been any acceleration
        if not self.speedChange:
            if self.speed > 0:
                self.speed -= self.acceleration / 2
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.acceleration / 2
                if self.speed > 0:
                    self.speed = 0
                
        self.speedChange = False
    
    """
    TURN
    Turns the wheels of the Vehicle, or the Vehicle itself (depending on implementation)
    """
    def turn(self, direction):
        # self.tireAngle = ((self.tireAngle + self.maxTireAngle + (self.turnSpeed * direction)) % (self.maxTireAngle * 2)) - self.maxTireAngle

        self.vehicleAngle = (self.vehicleAngle + (self.turnSpeed * direction)) % 360

    """
    ACCELERATE
    Accelerates Vehicle in direction of movement
    """
    def accelerate(self, direction):
        # self.speed = ((self.speed + self.maxSpeed + (self.acceleration * direction)) % (self.maxSpeed * 2)) - self.maxSpeed
        self.speed = self.speed + (self.acceleration * direction)
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        elif self.speed < -self.maxSpeed:
            self.speed = -self.maxSpeed
            
        self.speedChange = True

    
    
    
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
    def move(self, rect):
        pass
    
    
    
###############################################
###############  WARP WHEN HIT  ###############
###############################################
class WarpWhenHit(Navigator):
    def __init__(self, locations) -> None:
        super().__init__()
        self.warpPointOptions = locations
        self.needToMove = False
        
    """
    MOVE
    Chooses a warp point from among the internal list of options
    that is different than the position given
    """
    def move(self, rect):
        if self.needToMove:
            newSpot = Point(rect.x, rect.y)
            while newSpot.x == rect.x and newSpot.y == rect.y:
                newSpot = self.warpPointOptions[random.randint(0, len(self.warpPointOptions)-1)]
            
            rect.x = newSpot.x
            rect.y = newSpot.y

            self.needToMove = False
    
    
    
#####################################################
###############  WARP WHEN HIT TIMED  ###############
#####################################################
class WarpWhenHitTimed(WarpWhenHit):
    def __init__(self, locations) -> None:
        super().__init__()
        self.warpPointOptions = locations
        
    """
    MOVE
    Chooses a warp point from among the internal list of options
    that is different than the position given
    """
    def move(self, rect):
        return super().move()
    
    
    
################################################
###############  CYCLE WHEN HIT  ###############
################################################
class CycleWhenHit(Navigator):
    def __init__(self, locations) -> None:
        super().__init__()
        self.targetPositions = locations
        self.currentIndex = 0
        
    """
    MOVE
    Cycles the currentIndex to the next position in the list,
    restarting at 0 when the end of the list is reached.
    """
    def move(self, rect):
        pass