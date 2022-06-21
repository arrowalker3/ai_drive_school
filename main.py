"""
AI DRIVING SCHOOL
"""

from errno import ENOMSG
import os
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

def testEnvironment():
    # Select map
    env = Environment()
    
    # Create map
    mapSuccess = env.createMap(f"maps/{selectMapFile()}")
    if mapSuccess:
        # While continue, run environment
        gameOver = False
        while not gameOver:
            reward, gameOver, score = env.playStep()
            # If game over, ask if reset environment to above step (within game)
    else:
        print(f"Something went wrong with trying to open the map file.")
        
def trainAI():
    print("Training AI option is still in development.")
    # Set FPS
    # Request filename to save NN settings
        # STRETCH - If file selected from settings folder, load state into Network
    # Request map from list
    # Create map
    # While continue:
        # Get starting state
        # Get move
        # playStep using action
        # get new state
        # train short memory
        # remember state information
        # if game over:
            # reset environment
            # train long memory
            # if new high score, save model
            # print any output
            
def runAI():
    print("Running AI option is still in development.")
    # Select NN settings filename from list
        # If no list, return to mode selection
        # Load settings into Model
    # Select map file from list
    # Create map
    # while continue:
        # get starting state
        # get move
        # playStep using action
        # if game over, reset environment and print any output
            
            

def main():
    # Request mode selection
    active = True
    while active:
        # choice = modeSelection()
        choice = "1"
        
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