from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Vehicle, Target, Wall
from copy import copy
import json

class MapManager:
    def __init__(self) -> None:
        self.carStart = Point(0, 0)
        
    def createBorder(self):
        pass
        
    def createObjects(self, mapInfoString):
        mapInfoDict = json.loads(mapInfoString)
        
        # Create Vehicle
        self.carStart = Point(mapInfoDict["vehicleStart"]["x"], mapInfoDict["vehicleStart"]["y"])
        vehicle = Vehicle()
        vehicle.position = copy(self.carStart)
        
        # Create Target
        targetLocations = []
        for position in mapInfoDict["targetLocations"]:
            targetLocations.append(Point(position["x"], position["y"]))
            
        target = Target(targetLocations)
        
        # Collect wall positions and dimensions
        walls = []
        
        return vehicle, target, walls
        