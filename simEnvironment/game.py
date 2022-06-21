import pygame
from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Collidable
from simEnvironment.mapManager import MapManager

class Environment:
    def __init__(self) -> None:
        self.walls = []
        self.target = None
        self.vehicle = None
        self.maxFPS = 30
        self.mapManager = MapManager()

        # init display
        self.display = pygame.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
        pygame.display.set_caption('AI Driving School')
        self.clock = pygame.time.Clock()
        
        
        self.restart()
        
    def restart(self):
        pass
        
    """
    GET STATE
    Collects viewing data about the environment
    """
    def getState(self):
        viewingData = []
        
        return viewingData
    
    """
    CREATE MAP
    Opens given mapFile, and populates the environment based on data there
    """
    def createMap(self, mapFile):
        successful = True
        try:
            f = open(mapFile, "r")
            self.vehicle, self.target, self.walls = self.mapManager.createObjects(f.read())
            f.close()
        except:
            successful = False

        return successful
    
    """
    PLAY STEP
    Core of the game loop. Every action that happens each frame is called here
    """
    def playStep(self, action=[0, 0, 0, 0, 0, 0], playerDriven=True):
        reward = 0
        gameOver = False
        score = 0
        
        # If playerDriven, get action
        if playerDriven:
            action = self.getPlayerAction()
        self.getOtherUserEvents()
        
        # advance every object
        # check collisions
        # Update UI and clock
        self.clock.tick(self.maxFPS)
        
        return reward, gameOver, score

    """
    GET PLAYER ACTION
    The section of code for interpreting any input by the player
    """
    def getPlayerAction(self):
        action = [0, 0, 0, 0, 0, 0]
        
        return action
    
    def getOtherUserEvents(self):
        for event in pygame.event.get():
            # Need to check if the user has requested to close the window entirely
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    """
    DRAW
    Calls each object's draw function
    """
    def draw(self):
        # Walls
        # Target
        # Vehicle
        
        return None