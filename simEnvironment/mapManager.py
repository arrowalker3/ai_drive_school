from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Vehicle, Target, Wall
import pygame
from copy import copy
import json
import os

class MapManager:
    def __init__(self) -> None:
        self.carStart = Point(0, 0)
        
    def createBorder(self):
        pass
        
    def createObjects(self, mapInfoString):
        mapInfoDict = json.loads(mapInfoString)
        
        # Create Vehicle
        self.carStart = Point(mapInfoDict["vehicleStart"]["x"], mapInfoDict["vehicleStart"]["y"])
        image = pygame.image.load(os.path.join('simEnvironment', 'images', 'testCar.png'))
        vehicle = Vehicle(image)
        vehicle.rect.move_ip(self.carStart.x, self.carStart.y)
        
        # Create Target
        targetLocations = []
        for position in mapInfoDict["targetLocations"]:
            targetLocations.append(Point(position["x"], position["y"]))
            
        target = Target(targetLocations)
        
        # Collect wall positions and dimensions
        walls = []
        
        return vehicle, target, walls
        