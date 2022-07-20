# AI DRIVING SCHOOL

## Introduction

Machine learning has many uses in today’s world. It is often used to review data and make predictions based on past trends, and is able to be far more accurate than human counterparts following a similar process. That same methodolgy can be used to create real-time navigational systems, allowing autonomous movement of robots for tasks such as flying drones, maneuvering equipment in a warehouse, and even driving cars.

## Purpose

This project’s aim is to develop a navigational AI that can successfully and safely maneuver in a simulated environment. This AI will then be able to be transferred into any program that has the proper inputs.

## Scope

There are 3 primary focuses of this project: a simulation environment, a Neural Network, and an agent to facilitate communication between the other two. The project accomplishes the following:

- The simulation environment is a custom 2D environment for simplicity of communication with the agent.
- The simulation environment simulates simple physics, such as inertia and friction, with the AI controlling a car (can drive forward, backward, and turn)
- The AI has an endpoint it is trying to reach (simulating a goal or destination it needs to get to in the real world)
- The AI is saved to a file, which can then be copied and uploaded to a program that uses the same inputs and outputs.

The project does not:

- Involve any robotics (the application in this area is theoretical)
- Guarantee the most efficient route is always taken by the AI when navigating
- Guarantee the AI will never run into obstacles, though the number of collisions will be as low as possible

## Technologies Used

The project is made using:

- Visual Studio Code
- Python
- Pytorch – for the agent and Neural Network
- Pygame – for the simulated environment

## Other Notes

The finalized program was able to reach a point where the AI learns how to maneuver well enough that in training, it reached a score of over 80,000 targets reached and parked on without any crashes after about 1,000 simulations. The simulation was cut short at that point, so it potentially could have perpetually run without crashes.

Maps are saved using json files in the 'maps' folder, and AI settings are saved in the 'settings' folder. Maps are simply descriptions for the program showing where targets can appear, where the vehicle starts, and where walls are placed.