class Environment:
    def __init__(self) -> None:
        self.walls = []
        self.target = None
        self.vehicle = None
        self.maxFPS = 30
        
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

        return successful
    
    """
    PLAY STEP
    Core of the game loop. Every action that happens each frame is called here
    """
    def playStep(self, action, playerDriven=True):
        reward = 0
        gameOver = False
        score = 0
        
        # If playerDriven, get action
        # advance every object
        # check collisions
        
        return reward, gameOver, score

    """
    GET PLAYER ACTION
    The section of code for interpreting any input by the player
    """
    def getPlayerAction(self):
        action = [0, 0, 0, 0, 0, 0]
        
        return action

    """
    DRAW
    Calls each object's draw function
    """
    def draw(self):
        # Walls
        # Target
        # Vehicle
        
        return None