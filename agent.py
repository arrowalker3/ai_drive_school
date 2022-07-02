import torch
import random
import numpy as np
from collections import deque
from model import LinearQNet, QTrainer

MAX_MEMORY = 500_000        # We can remember at most this many moves and their results
BATCH_SIZE = 1000           # How many moves do we train from at a time (at max)?
LEARNING_RATE = 0.001       # How much do we adjust our strategy based on results?
RANDOM_CHANCE = 150          # How many games do we include random moves for exploring new options?
RANDOMNESS_DECIDER = 400
HIDDEN_LAYER_SIZE = 256
OUTPUT_SIZE = 6



#######################################
###############  AGENT  ###############
#######################################
class Agent:
    def __init__(self, viewingDataLen) -> None:
        self.numberOfGames = 0
        self.last50Games = deque(maxlen=50)
        self.epsilon = 0        # Controls randomness
        self.gamma = 0.9          # For model
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(viewingDataLen, HIDDEN_LAYER_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)
        
    def loadFromFile(self, filename="default.pth"):
        loadedCheckpoint = self.model.load(filename)
        agentData = loadedCheckpoint["agentData"]
        
        self.numberOfGames = agentData["epoch"]
        self.trainer.optimizer.load_state_dict(agentData["optimState"])
        
        return loadedCheckpoint
        
    def saveToFile(self, filename="default.pth", checkpointInfo={}):
        checkpointInfo["agentData"] = {
            "epoch": self.numberOfGames,
            "optimState": self.trainer.optimizer.state_dict()
        }
        
        self.model.save(filename, checkpointInfo)

    """
    GET ENV STATE
    Gets Viewing Data from environment, making any final adjustments as needed
    """
    def getEnvState(self, environment):
        state = np.array(environment.getState())
        
        return state

    """
    REMEMBER
    Adds state information that's given to memory as tuple
    """
    def remember(self, state, action, reward, nextState, gameOver):
        self.memory.append((state, action, reward, nextState, gameOver))

    """
    TRAIN LONG MEMORY
    Uses a large batch of state information from memory to train the model
    """
    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE)     # list of tuples
        else:
            miniSample = self.memory
            
        # Collect all pieces together to train all at once
        states, actions, rewards, nextStates, gameOvers = zip(*miniSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, gameOvers)

    """
    TRAIN SHORT MEMORY
    Uses the given state information to make a quick training pass on the model
    """
    def trainShortMemory(self, state, action, reward, nextState, gameOver):
        self.trainer.trainStep(state, action, reward, nextState, gameOver)

    """
    GET ACTION
    Uses the model to predict the best action to take during the current
    frame based on the Viewing Data
    """
    def getAction(self, state):
        finalMove = [0, 0, 0, 0, 0, 0]
        self.epsilon = RANDOM_CHANCE - self.numberOfGames
        
        # Random move (exploration)
        if random.randint(0, RANDOMNESS_DECIDER) < self.epsilon:
            driveMove = random.randint(0, 2)
            turnMove = random.randint(3, 5)
            
        # Actual decision (exploitation)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            drivePrediction = prediction[0:3]
            turnPrediction = prediction[3:6]
            
            driveMove = torch.argmax(drivePrediction).item()
            turnMove = torch.argmax(turnPrediction).item() + 3
            
        finalMove[driveMove] = 1
        finalMove[turnMove] = 1
        
        return finalMove
    
    # def getEpsilon(self):
        