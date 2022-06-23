# from abc import ABC, abstractmethod
import pygame
from simEnvironment.globalResources import Point, FORWARD, BACKWARD, LEFT, RIGHT
from simEnvironment.hurtbox import Circle, Rect
from simEnvironment.image import Sprite, RectShape, TargetShape
from simEnvironment.navigator import PlayerNav, Motionless, WarpWhenHit, WarpWhenHitTimed, CycleWhenHit

############################################
###############  COLLIDABLE  ###############
############################################
class Collidable(pygame.sprite.Sprite):
    def __init__(self, width=5, height=5, color=pygame.Color('white')) -> None:
        super().__init__()
        # Needed for Sprite class
        self.originalImage = pygame.Surface((width, height))
        self.image = self.originalImage
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()   # Determines position and basic collision box
        self.mask = pygame.mask.from_surface(self.image)    # Acts as the precise hurtbox, but needs the name "mask"
        
        # Navigator
        self.nav = Motionless()
        
        # Extra info
        self.hit = False
        
    """
    UPDATE
    Holds all movement logic and anything else that happens each frame
    """
    def update(self):
        self.nav.move(self.rect)

    """
    ON COLLISION
    The Collidable object can determine what happens when a collision occurs
    """
    def onCollision(self):
        return None
    
    """
    MOVE
    Calls nav's move function
    """
    def move(self):
        return None

        
        
#########################################
###############  VEHICLE  ###############
#########################################
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image) -> None:
        super().__init__()
        # Needed for Sprite class
        self.originalImage = image
        self.image = self.originalImage
        self.image.set_colorkey(pygame.Color('white'))
        
        self.rect = self.image.get_rect()   # Determines position and basic collision box
        self.mask = pygame.mask.from_surface(self.image)    # Acts as the precise hurtbox, but needs the name "mask"
        
        # Navigator
        # self.nav = Motionless()
        self.nav = PlayerNav()
        
        # Extra info
        self.hit = False
        self.action = [0, 0, 0, 0, 0, 0]

    """
    ON COLLISION
    Changes Vehicle status to not alive
    """
    def onCollision(self):
        return super().onCollision()
    
    """
    UPDATE
    For a Vehicle:
        - edit navigator variables based on action
        - call super
    """
    def update(self):
        # Six actions to check
        # [1, 0, 0, -, -, -] = Accelerate Forward
        if self.action[0] == 1:
            self.nav.accelerate(FORWARD)
        # [0, 1, 0, -, -, -] = Acclerate Backward
        elif self.action[1] == 1:
            self.nav.accelerate(BACKWARD)
        # [0, 0, 1, -, -, -] = No Acceleration
        
        # [-, -, -, 1, 0, 0] = Turn Left
        if self.action[3] == 1:
            self.nav.turn(LEFT)
            self.rotateImage()
        # [-, -, -, 0, 1, 0] = Turn Right
        elif self.action[4] == 1:
            self.nav.turn(RIGHT)
            self.rotateImage()
        # [-, -, -, 0, 0, 1] = No Turn
        
        self.nav.move(self.rect)
        
    """
    ROTATE IMAGE
    In the pygame sprite using an image, the image must be rotated any time the object rotates.
    """
    def rotateImage(self):
        center = self.rect.center
        self.image = pygame.transform.rotozoom(self.originalImage, self.nav.vehicleAngle, 1)
        self.rect = self.image.get_rect(center = center)
        
        # Rotate the mask for accurate collisions
        self.mask = pygame.mask.from_surface(self.image)
    


########################################
###############  TARGET  ###############
########################################
class Target(Collidable):
    def __init__(self, locations) -> None:
        super().__init__(width=60, height=60, color=pygame.Color('yellow'))
        # self.hurtbox = Circle()
        self.nav = WarpWhenHit(locations)

    """
    ON COLLISION
    Initiates process of moving target to next position, returns points
    """
    def onCollision(self):
        self.nav.needToMove = True
        
        return 1
    
    
    
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