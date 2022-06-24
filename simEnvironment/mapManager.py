from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Vehicle, Target, Wall
import pygame
from copy import copy
import json
import os

class MapManager:
    def __init__(self) -> None:
        self.carStart = Point(0, 0)
        self.targetStart = Point(0, 0)
        
    def createBorder(self):
        pass
        
    def createObjects(self, mapInfoString):
        mapInfoDict = json.loads(mapInfoString)
        
        # Create Vehicle
        self.carStart = Point(mapInfoDict["vehicleStart"]["x"], mapInfoDict["vehicleStart"]["y"])
        image = pygame.image.load(os.path.join('simEnvironment', 'images', 'testCar.png'))
        vehicle = Vehicle(image)
        
        # Create Target
        targetLocations = []
        for position in mapInfoDict["targetLocations"]:
            targetLocations.append(Point(position["x"], position["y"]))
            
        target = Target(targetLocations)
        self.targetStart = targetLocations[0]
        
        # Collect wall positions and dimensions
        walls = []
        
        # Move to starting locations
        self.moveToStartingLocations(vehicle, target)
        
        return vehicle, target, walls
    
    def moveToStartingLocations(self, vehicle: pygame.sprite.Sprite, target: pygame.sprite.Sprite):
        vehicle.rect.x = self.carStart.x
        vehicle.rect.y = self.carStart.y
        
        target.rect.x = self.targetStart.x
        target.rect.y = self.targetStart.y
        