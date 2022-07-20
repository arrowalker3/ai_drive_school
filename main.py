"""
AI DRIVING SCHOOL
"""

from genericpath import isfile
import os
from select import select

from simEnvironment.game import Environment
from agent import Agent
from collections import deque


def getSelection(title, itemList, prompt, quittable=False):
    print(title, "\n")
        
    if quittable:
        prompt += " ('q' to exit)" 
    
    selection = ""
    validChoice = False
    while not validChoice:
        for idx, item in enumerate(itemList):
            print(f'\t{idx+1}. {item}')

        selection = input(f"\n{prompt}: ")
        
        # Q to quit
        if quittable and selection.lower() == 'q':
            validChoice = True
            selection = 0
            
        else:
            try:
                selection = int(selection)
                if selection > 0 and selection <= len(itemList):
                    validChoice = True
            except ValueError as e:
                pass

            if not validChoice:
                errorMessage = "Please enter one of the ints shown above"
                if quittable:
                    errorMessage += "or 'q' to quit"
                print(f"{errorMessage}\n")

    return selection - 1
        
        


def modeSelection():
    modes = [
        "Test Environment (Player driven)",
        "Train AI",
        "Run AI without training"
    ]
    selection = getSelection("AI DRIVING SCHOOL", modes, "Enter mode selection here", quittable=True)
    
    return selection + 1

def selectMapFile():
    # STRETCH CHALLENGE: Provide multiple options of map files
    title = "MAP SELECTION"
    myPath = "./maps"
    files = [f.split(".")[0] for f in os.listdir(myPath) if os.path.isfile(os.path.join(myPath, f))]
    
    selection = getSelection(title, files, "Enter map choice here")
    
    return files[selection] + ".json"

def selectNetworkSettingsFile(trainEnv = False):
    title = "AI SETTINGS SELECTION"
    myPath = "./settings"
    files = [f.split(".")[0] for f in os.listdir(myPath) if os.path.isfile(os.path.join(myPath, f))]
    if trainEnv:
        files.append("Enter a new file name")
    
    if len(files) > 0:
        selection = getSelection(title, files, "Enter selection here")
        fileName = files[selection] + ".pth"
    else:
        fileName = "default.pth"
        
    moreTraining = False
    if trainEnv:
        if selection == len(files) - 1:
            valid = False
            while not valid:
                newFile = input("What is the name of the new file (don't add file type): ")
                
                if len(newFile.split(".")) > 1 or len(newFile.split("/")) > 1 or len(newFile.split("\\")) > 1:
                    print("No periods or slashes allowed")
                else:
                    valid = True
                    fileName = newFile + ".pth"
                    
        else:
            choice = input("Would you like to train this AI further? y/[n]: ")
            if choice.lower() == "y":
                moreTraining = True
    
    return fileName, moreTraining

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
            if gameOver:
                print("Restarting...")
                env.restart()
                gameOver = False
    else:
        print(f"Something went wrong with trying to open the map file.")
        
def trainAI():
    # print("Training AI option is still in development.")
    # Select map
    env = Environment()
    env.playerDriven = False
    env.maxFPS = 200
    
    # Create map
    mapSuccess = env.createMap(f"maps/{selectMapFile()}")
    # Set FPS
    # Request filename to save NN settings
    filename, continueTraining = selectNetworkSettingsFile(trainEnv=True)
    
        # STRETCH - If file selected from settings folder, load state into Network
    if mapSuccess:
        # Prep work
        env.setupEnv()
        agent = Agent(len(env.getState()))
        
        if continueTraining:
            saveData = agent.loadFromFile(filename)
            highScore = saveData["highScore"]
        else:
            highScore = 0
        lowestReward = 0
        highestReward = 0
        currReward = 0
        REWARD_MEMORY_LENGTH = 100
        rewardMemory = deque(maxlen=REWARD_MEMORY_LENGTH)
        
        
        # While continue:
        train = True
        while train:
            # Get starting state
            startingState = env.getState()
            
            # Get move
            action = agent.getAction(startingState)
            
            # playStep using action
            reward, gameOver, score = env.playStep(action)
            currReward += reward

            # get new state
            resultingState = env.getState()

            # remember state information
            agent.remember(startingState, action, reward, resultingState, gameOver)
            
            # train short memory
            # agent.trainShortMemory(startingState, action, reward, resultingState, gameOver)

            if gameOver:
                # reset environment
                env.restart()
                agent.numberOfGames += 1
                
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
                
                # train long memory
                agent.trainLongMemory()
                        
                if currReward < lowestReward:
                    lowestReward = currReward
                elif currReward > highestReward:
                    highestReward = currReward
                    
                # Save reward and update epsilon in agent
                rewardMemory.append(currReward)
                agent.adjustEpsilon(list(rewardMemory)[:REWARD_MEMORY_LENGTH//2], list(rewardMemory)[REWARD_MEMORY_LENGTH//2:])
                    
                # print any output
                print(f'Simulation {agent.numberOfGames} results, {score} points. Record: {highScore}. Low reward: {lowestReward:.2f}. High reward: {highestReward:.2f}. Curr: {currReward:.2f}')
                currReward = 0

            else:   # gameOver == False
                # If it is doing so well that it doesn't actually die, this still saves the AI
                if score > highScore+100:   # Only if it does extremely better than previous attempts
                    highScore = score
                    print(f'Running simulation {agent.numberOfGames}, alive with new record of {highScore} points.')
                    saveData = {
                        "highScore": highScore
                    }
                    try:
                        agent.saveToFile(filename, saveData)
                    except Exception as e:
                        print(e, "\n\n Missed a save")
                    
                
    else:
        print(f"Something went wrong with trying to open the map file.")
            
def runAI():
    print("Running AI option is still in development.")
    env = Environment()
    env.playerDriven = False
    
    # Select NN settings filename
    pthFilename, _ = selectNetworkSettingsFile()
    while not os.path.exists(os.path.join('.','settings', pthFilename)):
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
        choice = modeSelection()
        # choice = "3"
        
        # If Test Environment (1)
        if choice == 1:
            testEnvironment()
        # If Train AI Environment (2)
        elif choice == 2:
            trainAI()
        # If Run AI Environment (3)
        elif choice == 3:
            runAI()
        else:
            active = False
        


if __name__ == "__main__":
    main()