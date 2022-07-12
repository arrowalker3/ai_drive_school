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
        # Driving decision layers
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, hiddenSize)
        # self.linear2_5 = nn.Linear(hiddenSize, hiddenSize)
        self.linear3 = nn.Linear(hiddenSize, outputSize)
        
    """
    FORWARD
    The forward function of the network: makes a prediction
    of most beneficial move based on inputs
    """
    def forward(self, x):
        # Driving prediction
        drivePrediction = F.leaky_relu(self.linear1(x))
        drivePrediction = F.leaky_relu(self.linear2(drivePrediction))
        # drivePrediction = F.relu(self.linear2_5(drivePrediction))
        drivePrediction = self.linear3(drivePrediction)
        
        return drivePrediction
    
    """
    SAVE
    Saves the Neural Network to be used later
    """
    def save(self, fileName='default.pth', infoToSave={}):
        # Add the model to the information we're saving
        infoToSave["modelState"] = self.state_dict()
        
        modelFolderPath = './settings'
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)
            
        fileName = os.path.join(modelFolderPath, fileName)
        
        torch.save(infoToSave, fileName)
    
    """
    LOAD
    Using the given file name, opens file and fills out
    weights of Neural Network
    """
    def load(self, fileName):
        modelFolderPath = './settings'
        
        if not os.path.exists(modelFolderPath):
            pass

        fileName = os.path.join(modelFolderPath, fileName)
        
        loadedCheckpoint = torch.load(fileName)
        
        self.load_state_dict(loadedCheckpoint["modelState"])
        self.eval()
        
        return loadedCheckpoint
    
    
    
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
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        
        # For short term training, unsqueeze data to match long term training shapes
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            nextState = torch.unsqueeze(nextState, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            gameOver = (gameOver, )
            
        # Predict using the current model
        pred = self.model(state)
        
        # Find Q_new and adjust weights accordingly
        target = pred.clone()           # Copy of the predictions for later
        
        # For every move in memory that we're given...
        for idx in range(len(gameOver)):
            # What is the reward resulting from the predicted move?
            Q_new_drive = reward[idx]
            Q_new_turn = reward[idx]
            
            # If the next move didn't cause a game over, ...
            if not gameOver[idx]:
                # What would the reward be with the current model? Will the next state we move to after be beneficial?
                nextStateResults = self.model(nextState[idx])
                Q_new_drive = reward[idx] + self.gamma * torch.max(nextStateResults[0:3])
                Q_new_turn = reward[idx] + self.gamma * torch.max(nextStateResults[3:6])
                # "gamma" above determines how much a single example affects the neural network
                
            # Whatever the result of the chosen action was, we want the neural net to be able to predict those results
            currAction = action[idx]
            driveAction = currAction[0:3]
            turnAction = currAction[3:6]
            target[idx][torch.argmax(driveAction).item()] = Q_new_drive
            target[idx][torch.argmax(turnAction).item() + 3] = Q_new_turn
        
        # Zero out weights from training
        self.optimizer.zero_grad()
        
        # Determine loss
        loss = self.criterion(target, pred)
        
        # Modify weights in model
        loss.backward()
        
        self.optimizer.step()

    