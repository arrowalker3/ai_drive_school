import torch
import random
import numpy as np
from collections import deque
from model import LinearQNet, QTrainer

#######################################
###############  AGENT  ###############
#######################################
class Agent:
    def __init__(self) -> None:
        self.numberOfGames = 0
        self.epsilon = 0        # Controls randomness
        self.gamma = 0          # For model
        self.memory = deque()
        self.model = None
        self.trainer = None

    """
    GET ENV STATE
    Gets Viewing Data from environment, making any final adjustments as needed
    """
    def getEnvState(self, environment):
        state = np.array()
        
        return state

    """
    REMEMBER
    Adds state information that's given to memory as tuple
    """
    def remember(self, state, action, reward, nextState, gameOver):
        return None

    """
    TRAIN LONG MEMORY
    Uses a large batch of state information from memory to train the model
    """
    def trainLongMemory(self):
        return None

    """
    TRAIN SHORT MEMORY
    Uses the given state information to make a quick training pass on the model
    """
    def trainShortMemory(self, state, action, reward, nextState, gameOver):
        return None

    """
    GET ACTION
    Uses the model to predict the best action to take during the current
    frame based on the Viewing Data
    """
    def getAction(self, state):
        finalMove = [0, 0, 0, 0, 0, 0]
        
        return finalMove