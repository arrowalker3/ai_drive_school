from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Vehicle, Target, Wall
from simEnvironment.navigator import Navigator, PlayerNav, Motionless, WarpWhenHit, WarpWhenHitTimed, CycleWhenHit, TimedCycleWhenHit
import pygame
from copy import copy
import json
import os

from simEnvironment.navigator import PlayerNav

class MapManager:
    def __init__(self) -> None:
        self.carStart = Point(0, 0)
        self.targetStart = Point(0, 0)
        
    def createBorder(self):
        borders = []
        defaultThickness = 20
        shiftAmount = 5
        
        # Left
        wall = Wall(defaultThickness, HEIGHT_BOARD)
        wall.rect.x = -shiftAmount
        borders.append(wall)
        
        # Right
        wall = Wall(defaultThickness, HEIGHT_BOARD)
        wall.rect.x = WIDTH_BOARD - (defaultThickness - shiftAmount)
        borders.append(wall)
        
        # Top
        wall = Wall(WIDTH_BOARD, defaultThickness)
        wall.rect.y = -shiftAmount
        borders.append(wall)
        
        # Bottom
        wall = Wall(WIDTH_BOARD, defaultThickness)
        wall.rect.y = HEIGHT_BOARD - (defaultThickness - shiftAmount)
        borders.append(wall)
        
        return borders
        
        
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
            
        navType = mapInfoDict["targetNavType"]
        if navType == "cycle":
            navigator = CycleWhenHit(targetLocations)
        elif navType == "cycle-timed":
            navigator = TimedCycleWhenHit(targetLocations)
        elif navType == "warp-timed":
            navigator = WarpWhenHitTimed(targetLocations)
        else:       # navType = "default"
            navigator = WarpWhenHit(targetLocations)
            
        target = Target(navigator)
        self.targetStart = targetLocations[0]
        
        # Collect wall positions and dimensions
        walls = []
        for wall in mapInfoDict["walls"]:
            newWall = Wall(wall["width"], wall["height"],
                           wall["x"], wall["y"])
            
            walls.append(newWall)
        
        # Move to starting locations
        self.moveToStartingLocations(vehicle, target)
        
        return vehicle, target, walls
    
    def moveToStartingLocations(self, vehicle: pygame.sprite.Sprite, target: pygame.sprite.Sprite):
        vehicle.reset(self.carStart.x, self.carStart.y)
        
        target.restart()
        # target.rect.x = self.targetStart.x
        # target.rect.y = self.targetStart.y
        