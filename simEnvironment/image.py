from abc import ABC, abstractmethod

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
    def __init__(self) -> None:
        super().__init__()
    """
    DRAW
    Draws image to the window at position and rotation
    """
    def draw(self, position, rotation):
        return None
    
    
    
##############################################
###############  TARGET SHAPE  ###############
##############################################
class RectShape(Image):
    def __init__(self) -> None:
        super().__init__()
    """
    DRAW
    Draws image to the window at position and rotation
    """
    def draw(self, position, rotation):
        return None