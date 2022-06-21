from abc import ABC, abstractmethod

import pygame

#######################################
###############  IMAGE  ###############
#######################################
class Image(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.color = (0, 0, 0)
    """
    DRAW
    Draws image to the window at position and rotation
    """
    @abstractmethod
    def draw(self, position, rotation):
        return None
    
    
    
########################################
###############  SPRITE  ###############
########################################
class Sprite(Image):
    def __init__(self) -> None:
        super().__init__()
        self.image = None
    """
    DRAW
    Draws image to the window at position and rotation
    """
    def draw(self, position, rotation):
        return None
    
    
    
############################################
###############  RECT SHAPE  ###############
############################################
class RectShape(Image):
    def __init__(self, w, h) -> None:
        super().__init__()
        self.w = w
        self.h = h
    """
    DRAW
    Draws image to the window at position and rotation
    """
    def draw(self, position, rotation):
        pygame.draw.rect()
    
    
    
##############################################
###############  TARGET SHAPE  ###############
##############################################
class TargetShape(Image):
    def __init__(self, radius) -> None:
        super().__init__()
        self.radius = radius
    """
    DRAW
    Draws image to the window at position and rotation
    """
    def draw(self, position, rotation):
        return None