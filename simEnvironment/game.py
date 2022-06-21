import pygame
from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Collidable
from simEnvironment.mapManager import MapManager

#############################################
###############  ENVIRONMENT  ###############
#############################################
class Environment:
    def __init__(self, startingFPS=30) -> None:
        self.allSpritesList = pygame.sprite.Group()
        self.wallsList = pygame.sprite.Group()
        # self.target = None
        # self.vehicle = None
        self.vehicleGroup = pygame.sprite.GroupSingle()
        self.targetGroup = pygame.sprite.GroupSingle()
        self.maxFPS = startingFPS
        self.mapManager = MapManager()

        # init display
        self.display = pygame.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
        pygame.display.set_caption('AI Driving School')
        self.clock = pygame.time.Clock()
        
        self.timer = 0
        self.heldKeys = set()
        
        
        self.restart()
        
    """
    RESTART
    Set all sprites back to starting positions, score to 0, and anything else
    that needs to happen
    """
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
            vehicle, target, walls = self.mapManager.createObjects(f.read())
            f.close()
            
            # Add results to the game
            for object in walls:
                self.wallsList.add(object)
                self.allSpritesList.add(object)
            self.targetGroup.sprite = target
            self.allSpritesList.add(target)
            self.vehicleGroup.sprite = vehicle
            self.allSpritesList.add(vehicle)
        except Exception as e:
            print(e)
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
        
        # Give action to vehicle
        self.vehicleGroup.sprite.action = action
        
        # advance every object
        self.allSpritesList.update()

        # Update UI and clock
        self.display.fill(pygame.Color('green'))
        self.allSpritesList.draw(self.display)
        self.clock.tick(self.maxFPS)
        
        pygame.display.flip()
        
        # check collisions
        # Vehicle hit target
        targetCollisions = pygame.sprite.spritecollide(self.vehicleGroup.sprite, self.targetGroup, False, pygame.sprite.collide_mask)
        for target in targetCollisions:
            target.onCollision()
        
        return reward, gameOver, score

    """
    GET PLAYER ACTION
    The section of code for interpreting any input by the player
    """
    def getPlayerAction(self):
        action = [0, 0, 0, 0, 0, 0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
            elif event.type == pygame.KEYDOWN:
                self.heldKeys.add(event.key)
                
            elif event.type == pygame.KEYUP:
                if event.key in self.heldKeys:
                    self.heldKeys.remove(event.key)
                
        # Check held keys
        for x in self.heldKeys:
            if x == pygame.K_UP:
                action[0] = 1
            elif x == pygame.K_DOWN:
                action[1] = 1
            if x == pygame.K_LEFT:
                action[3] = 1
            elif x == pygame.K_RIGHT:
                action[4] = 1
        
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