import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os   # To save the model

##############################################
###############  LINEAR Q NET  ###############
##############################################
class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize) -> None:
        super().__init__()
        
    """
    FORWARD
    The forward function of the network: makes a prediction
    of most beneficial move based on inputs
    """
    def forward(self, x):
        drivePrediction = [0, 0, 0]
        turnPrediction = [0, 0, 0]
        
        return drivePrediction, turnPrediction
    
    """
    SAVE
    Saves the Neural Network to be used later
    """
    def save(self, fileName):
        return None
    
    """
    LOAD
    Using the given file name, opens file and fills out
    weights of Neural Network
    """
    def load(self, fileName):
        return None
    
    
    
###########################################
###############  Q TRAINER  ###############
###########################################
class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.learningRate = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.learningRate)
        self.criterion = nn.MSELoss()
        
    """
    TRAIN STEP
    Performs needed steps for training model, both short
    and long term
    """
    def trainStep(self, state, action, reward, nextState, gameOver):
        # Convert values to tensors
        # For short term training, unsqueeze data to match long term training shapes
        # Predict using the current model
        # For each type of output (drive and turn), find Q_new and adjust weights accordingly
        # Zero out weights from training
        # Determine loss
        # Modify weights in model
        
        return None

    