from abc import ABC, abstractmethod
import math
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
    
    """
    COLLIDED
    A function to be called when a collision has occurred
    """
    def collided(self):
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
        self.turnSpeed = 12
        self.acceleration = 0.75
        self.maxSpeed = 10
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
        
    """
    APPLY FRICTION
    Slow the object down to a complete stop.
    """
    def applyFriction(self):
        # Only apply if there hasn't been any acceleration
        if not self.speedChange:
            if self.speed > 0:
                self.speed -= self.acceleration / 1.5
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.acceleration / 1.5
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
        
    """
    RESTART
    Reset important variables to their starting values.
    """
    def restart(self):
        self.speed = 0
        self.vehicleAngle = 0
        self.tireAngle = 0
        self.speedChange = False

    
    
    
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
        self.targetPositions = locations
        self.needToMove = False
        
    """
    MOVE
    Chooses a warp point from among the internal list of options
    that is different than the position given
    """
    def move(self, rect, randomize=True):
        if self.needToMove:
            newSpot = self.targetPositions[random.randint(0, len(self.targetPositions)-1)]
            if randomize:
                while newSpot.x == rect.x and newSpot.y == rect.y:
                    newSpot = self.targetPositions[random.randint(0, len(self.targetPositions)-1)]
            
            rect.x = newSpot.x
            rect.y = newSpot.y

            self.needToMove = False
            
    """
    COLLIDED
    Warping object is triggered to move on a collision
    """
    def collided(self):
        self.needToMove = True
    
    """
    RESTART
    Set up warping object at a random position
    """
    def restart(self, rect):
        self.needToMove = True
        self.move(rect, False)
    
    
    
#####################################################
###############  WARP WHEN HIT TIMED  ###############
#####################################################
class WarpWhenHitTimed(WarpWhenHit):
    def __init__(self, locations, timerLength=30) -> None:
        super().__init__(locations)
        self.timer = 0
        self.runTimer = False
        self.timerLength = timerLength
        
    """
    MOVE
    If the timer is running, once time is up move the object
    """
    def move(self, rect, randomized=True):
        if self.runTimer:
            self.timer += 1
            if self.timer >= self.timerLength:
                super().move(rect, randomized)
                self.runTimer = False
                self.timer = 0
                self.timerLength = random.randint(1, 6) * 10    # Next target's timer lasts 10, 20, ..., or 60 frames
                
    """
    RESTART
    Set up so warping object is moved to random position at the start
    """
    def restart(self, rect):
        self.timer = self.timerLength
        self.runTimer = True
        super().restart(rect)
                
    """
    COLLIDED
    Start timer on collision
    """
    def collided(self):
        super().collided()
        self.runTimer = True
    
    
    
################################################
###############  CYCLE WHEN HIT  ###############
################################################
class CycleWhenHit(WarpWhenHit):
    def __init__(self, locations) -> None:
        super().__init__(locations)
        self.currentIndex = 0
        
    """
    MOVE
    Cycles the currentIndex to the next position in the list,
    restarting at 0 when the end of the list is reached.
    """
    def move(self, rect):
        if self.needToMove:
            self.currentIndex = (self.currentIndex + 1) % len(self.targetPositions)
            rect.x = self.targetPositions[self.currentIndex].x
            rect.y = self.targetPositions[self.currentIndex].y
        
        self.needToMove = False
        
    """
    RESTART
    Set up so object will be moved to starting position
    """
    def restart(self, rect):
        self.currentIndex = len(self.targetPositions)-1
        self.needToMove = True
        self.move(rect)
    
    
    
######################################################
###############  CYCLE WHEN HIT TIMED  ###############
######################################################
class TimedCycleWhenHit(CycleWhenHit):
    def __init__(self, locations, timerLength=30) -> None:
        super().__init__(locations)
        self.timer = 0
        self.runTimer = False
        self.timerLength = timerLength
        
    """
    MOVE
    Move only when timer has been activated and at the proper value
    """
    def move(self, rect):
        if self.runTimer:
            self.timer += 1
            if self.timer >= self.timerLength:
                super().move(rect)
                self.runTimer = False
                self.timer = 0
                self.timerLength = random.randint(1, 6) * 10    # Next target's timer lasts 10, 20, ..., or 60 frames
                
    """
    RESTART
    Move object to starting position
    """
    def restart(self, rect):
        self.timer = self.timerLength
        self.runTimer = True
        super().restart(rect)
                
    """
    COLLIDED
    Start timer on collision
    """
    def collided(self):
        super().collided()
        self.runTimer = True