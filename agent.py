import torch
import random
import numpy as np
from collections import deque
from model import LinearQNet, QTrainer
from statistics import mean

MAX_MEMORY = 500_000        # We can remember at most this many moves and their results
BATCH_SIZE = 2000           # How many moves do we train from at a time (at max)?
LEARNING_RATE = 0.003       # How much do we adjust our strategy based on results?
EPSILON_CAP = 0.8
N_RANDOM_GAMES = 500
HIDDEN_LAYER_SIZE = 256
OUTPUT_SIZE = 6
TICK_ROLLOVER = 50



#######################################
###############  AGENT  ###############
#######################################
class Agent:
    def __init__(self, viewingDataLen) -> None:
        self.numberOfGames = 0
        self.last50Games = deque(maxlen=50)
        self.epsilonTicks = 0
        self._epsilon = EPSILON_CAP        # Controls randomness
        self.gamma = 0.9          # For trainer
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(viewingDataLen, HIDDEN_LAYER_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)
        
    
    @property
    def epsilon(self):
        return self._epsilon
    
    @epsilon.setter
    def epsilon(self, x):
        self._epsilon = x
        if self._epsilon > EPSILON_CAP:
            self._epsilon = EPSILON_CAP
        elif self._epsilon < 0:
            self._epsilon = 0
        
    def loadFromFile(self, filename="default.pth"):
        loadedCheckpoint = self.model.load(filename)
        agentData = loadedCheckpoint["agentData"]
        
        self.numberOfGames = agentData["epoch"]
        self._epsilon = agentData["epsilon"]
        self.trainer.optimizer.load_state_dict(agentData["optimState"])
        
        return loadedCheckpoint
        
    def saveToFile(self, filename="default.pth", checkpointInfo={}):
        checkpointInfo["agentData"] = {
            "epoch": self.numberOfGames,
            "optimState": self.trainer.optimizer.state_dict(),
            "epsilon": self._epsilon
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
        # self.epsilon = RANDOM_CHANCE - self.numberOfGames
        
        # Random move (exploration)
        if random.random() < self.epsilon:
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
    
    def adjustEpsilon(self, oldRewards, recentRewards, dynamic=False):
        if dynamic:
            # Get average of old rewards
            oldAverage = mean(oldRewards) if len(oldRewards) > 0 else 0
            # Get average of recent rewards
            recentAverage = mean(recentRewards) if len(recentRewards) > 0 else 0
            self.epsilonTicks += 1
            
            if self.epsilonTicks > TICK_ROLLOVER:
                if recentAverage > oldAverage:  # Doing well, lower epsilon
                    self.epsilon -= 0.025
                    if self.epsilon < 0:
                        self.epsilon = 0
                else:                           # Doing worse, raise epsilon
                    self.epsilon += 0.025
                
                self.epsilonTicks = 0
        else:
            self.epsilon = EPSILON_CAP - (EPSILON_CAP * (self.numberOfGames / N_RANDOM_GAMES))