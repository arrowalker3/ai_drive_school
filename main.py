"""
AI DRIVING SCHOOL
"""

import os

print(os.path.abspath("."))


def main():
    pass
    # Quick set up: Agent, Environment, Model
    # Request mode selection
    # If Test Environment:
        # Select map
        # Create map
        # While continue, run environment
        # If game over, ask if reset environment to above step
    # If Train AI Environment:
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
    # If Run AI Environment:
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
    # Return to mode selection if continue


if __name__ == "__main__":
    main()