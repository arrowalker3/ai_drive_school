"""
AI DRIVING SCHOOL
"""

from errno import ENOMSG
import os
import pygame
from select import select

from simEnvironment.game import Environment
from model import LinearQNet, QTrainer
from agent import Agent

def modeSelection():
    print("""AI DRIVING SCHOOL
        
        Please choose a mode:
        1. Test Environment (Player driven)
        2. Train AI
        3. Run AI without training
        """)
    
    return input("Enter your selection here: ")

def selectMapFile():
    # STRETCH CHALLENGE: Provide multiple options of map files
    return "level1.json"

def selectNetworkSettingsFile():
    return "default.pth"

def testEnvironment():
    # Select map
    env = Environment()
    env.playerDriven = True
    
    # Create map
    mapSuccess = env.createMap(os.path.join('maps', selectMapFile()))
    # mapSuccess = env.createMap(f'maps/{selectMapFile()}')
    if mapSuccess:
        env.setupEnv()
        
        # While continue, run environment
        gameOver = False
        while not gameOver:
            reward, gameOver, score = env.playStep()
            # If game over, ask if reset environment to above step (within game)
    else:
        print(f"Something went wrong with trying to open the map file.")
        
def trainAI():
    print("Training AI option is still in development.")
    # Select map
    env = Environment()
    env.playerDriven = False
    env.maxFPS = 200
    
    # Create map
    mapSuccess = env.createMap(f"maps/{selectMapFile()}")
    # Set FPS
    # Request filename to save NN settings
    filename = selectNetworkSettingsFile()
    
        # STRETCH - If file selected from settings folder, load state into Network
    if mapSuccess:
        # Prep work
        env.setupEnv()
        agent = Agent(len(env.getState()))
        highScore = 0
        
        # While continue:
        train = True
        while train:
            # Get starting state
            startingState = env.getState()
            
            # Get move
            action = agent.getAction(startingState)
            
            # playStep using action
            reward, gameOver, score = env.playStep(action)

            # get new state
            resultingState = env.getState()
            
            # train short memory
            agent.trainShortMemory(startingState, action, reward, resultingState, gameOver)

            # remember state information
            agent.remember(startingState, action, reward, resultingState, gameOver)

            if gameOver:
                # reset environment
                env.restart()
                agent.numberOfGames += 1
                
                # train long memory
                agent.trainLongMemory()
                
                # if new high score, save model
                if score > highScore:
                    highScore = score
                saveData = {
                    "highScore": highScore
                }
                try:
                    agent.saveToFile(filename, saveData)
                except Exception as e:
                    print(e, "\n\n Missed a save")
                    
                # print any output
                print(f'Simulation {agent.numberOfGames}, {score} points. Record: {highScore}')
                
    else:
        print(f"Something went wrong with trying to open the map file.")
            
def runAI():
    print("Running AI option is still in development.")
    env = Environment()
    env.playerDriven = False
    
    # Select NN settings filename
    pthFilename = selectNetworkSettingsFile()
    while not os.path.exists(os.path.join('./settings', pthFilename)):
        print("File doesn't exist")
        pthFilename = selectNetworkSettingsFile()
    
    # Select map file from list
    mapSuccess = env.createMap(f"maps/{selectMapFile()}")
        
    if mapSuccess:
        # Prep work
        env.setupEnv()
        agent = Agent(len(env.getState()))
        saveData = agent.loadFromFile(pthFilename)
        highScore = saveData["highScore"]
        
        # While continue:
        run = True
        while run:
            # Get starting state
            startingState = env.getState()
            
            # Get move
            action = agent.getAction(startingState)
            
            # playStep using action
            reward, gameOver, score = env.playStep(action)

            if gameOver:
                # reset environment
                env.restart()
                    
                # print any output
                print(f'Game over! {score} points. Record from training: {highScore}')
                
    else:
        print(f"Something went wrong with trying to open the map file.")
            
            

def main():
    # Request mode selection
    active = True
    # pygame.init()
    while active:
        # choice = modeSelection()
        choice = "3"
        
        # If Test Environment (1)
        if choice == "1":
            testEnvironment()
        # If Train AI Environment (2)
        elif choice == "2":
            trainAI()
        # If Run AI Environment (3)
        elif choice == "3":
            runAI()
        else:
            print("Couldn't understand the selection, please choose either 1, 2, or 3")
                
        # Return to mode selection if continue
        reselectMode = input("Would you like to start another mode? [y]/n: ")
        if reselectMode.lower() == "n":
            active = False
        


if __name__ == "__main__":
    main()