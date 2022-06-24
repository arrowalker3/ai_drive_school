import pygame
import math
import os
from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Collidable
from simEnvironment.mapManager import MapManager

# Choosing what goes into Viewing Data
VEHICLE_SPEED_INCLUDED = True
VEHICLE_ANGLE_INCLUDED = True
TARGET_DIRECTION_INCLUDED = True
TARGET_DISTANCE_INCLUDED = True

pygame.init()
font = pygame.font.Font(os.path.join('simEnvironment', 'arial.ttf'), 16)
# font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.get_default_font()

#############################################
###############  ENVIRONMENT  ###############
#############################################
class Environment:
    def __init__(self, startingFPS=30) -> None:
        self.allSpritesList = pygame.sprite.Group()
        self.wallsList = pygame.sprite.Group()
        self.vehicleGroup = pygame.sprite.GroupSingle()
        self.targetGroup = pygame.sprite.GroupSingle()
        self.mapManager = MapManager()

        self.playerDriven = False
        self.maxFPS = startingFPS
        
        self.stateLabels = []
        
        self.timer = 0
        self.heldKeys = set()
        
        
    def setupEnv(self):
        # init display
        self.display = pygame.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
        pygame.display.set_caption('AI Driving School')
        self.clock = pygame.time.Clock()
        self.restart()
            
    """
    RESTART
    Set all sprites back to starting positions, score to 0, and anything else
    that needs to happen
    """
    def restart(self):
        self.frameCount = 0
        self.score = 0
        
        self.mapManager.moveToStartingLocations(self.vehicleGroup.sprite, self.targetGroup.sprite)
        
    """
    GET STATE
    Collects viewing data about the environment
    """
    def getState(self, normalize=True):
        viewingData = []
        self.stateLabels.clear()
        
        if VEHICLE_SPEED_INCLUDED:
            # Get Speed
            speed = self.vehicleGroup.sprite.nav.speed

            # Normalize
            if normalize:
                speed = (speed / (self.vehicleGroup.sprite.nav.maxSpeed * 2)) + 0.5
            
            # Add to data
            viewingData.append(speed)
            self.stateLabels.append('Speed:')
        
        if VEHICLE_ANGLE_INCLUDED:
            # Get Angle
            vehicleAngle = self.vehicleGroup.sprite.nav.vehicleAngle
            
            # Normalize
            if normalize:
                vehicleAngle /= 360
            
            # Add to data
            viewingData.append(vehicleAngle)
            self.stateLabels.append('V_Angle:')
        
        if TARGET_DIRECTION_INCLUDED:
            # Get Direction relative to vehicle angle
            targetDirection = self.getAngleFromPoints()

            # Normalize
            if normalize:
                targetDirection += 180
                targetDirection /= 360
                
            # Add to data
            viewingData.append(targetDirection)
            self.stateLabels.append('T_Direction:')
        
        if TARGET_DISTANCE_INCLUDED:
            # Get Distance
            targetPosition = self.targetGroup.sprite.rect.center
            vehiclePosition = self.vehicleGroup.sprite.rect.center
            targetDistance = math.sqrt((targetPosition[0] - vehiclePosition[0])**2 + (targetPosition[1] - vehiclePosition[1])**2)
            
            # Normalize
            if normalize:
                maxDistance = math.sqrt(WIDTH_BOARD**2 + HEIGHT_BOARD**2)
                targetDistance /= maxDistance
                
            # Add to data
            viewingData.append(targetDistance)
            self.stateLabels.append('T_Distance:')
        
        return viewingData
    
    """
    CREATE MAP
    Opens given mapFile, and populates the environment based on data there
    """
    def createMap(self, mapFile):
        successful = True
        try:
            f = open(mapFile, "r")
            vehicle, target, walls = self.mapManager.createObjects(f.read())
            f.close()
            
            # Add results to the game
            for object in walls:
                self.wallsList.add(object)
                self.allSpritesList.add(object)
            self.targetGroup.sprite = target
            self.allSpritesList.add(target)
            self.vehicleGroup.sprite = vehicle
            self.allSpritesList.add(vehicle)
            
        except Exception as e:
            print(e)
            successful = False

        return successful
    
    """
    PLAY STEP
    Core of the game loop. Every action that happens each frame is called here
    """
    def playStep(self, action=[0, 0, 0, 0, 0, 0]):
        reward = 0
        gameOver = False
        # self.score = 0
        
        # If playerDriven, get action
        if self.playerDriven:
            action = self.getPlayerAction()
        else:
            self.frameCount += 1
            if self.frameCount > (100 * (self.score + 1)):
                reward -= 10
                gameOver = True
                
                return reward, gameOver, self.score
            
        self.getOtherUserEvents()
        
        # Give action to vehicle
        self.vehicleGroup.sprite.action = action
        
        # advance every object
        self.allSpritesList.update()

        # Update UI and clock
        self.draw()
        self.clock.tick(self.maxFPS)
        
        # check collisions
        # Vehicle hit target
        targetCollisions = pygame.sprite.spritecollide(self.vehicleGroup.sprite, self.targetGroup, False, pygame.sprite.collide_mask)
        for target in targetCollisions:
            self.score += target.onCollision()
            reward += 10
        
        return reward, gameOver, self.score

    """
    GET PLAYER ACTION
    The section of code for interpreting any input by the player
    """
    def getPlayerAction(self):
        action = [0, 0, 0, 0, 0, 0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
            elif event.type == pygame.KEYDOWN:
                self.heldKeys.add(event.key)
                
            elif event.type == pygame.KEYUP:
                if event.key in self.heldKeys:
                    self.heldKeys.remove(event.key)
                
        # Check held keys
        for x in self.heldKeys:
            if x == pygame.K_UP:
                action[0] = 1   # [1, 0, 0, -, -, -]
            elif x == pygame.K_DOWN:
                action[1] = 1   # [0, 1, 0, -, -, -]
                
            if x == pygame.K_LEFT:
                action[3] = 1   # [-, -, -, 1, 0, 0]
            elif x == pygame.K_RIGHT:
                action[4] = 1   # [-, -, -, 0, 1, 0]
        
        return action
    
    def getOtherUserEvents(self):
        for event in pygame.event.get():
            # Need to check if the user has requested to close the window entirely
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
    """
    DRAW
    Draws everything to the display
    """
    def draw(self):
        self.display.fill(pygame.Color('green'))
        self.allSpritesList.draw(self.display)
        
        if self.playerDriven:
            viewingData = self.getState(normalize=True)
            index = 0
            
            for stat in viewingData:
                text = font.render(f'{self.stateLabels[index]} {stat:.2f}', True, pygame.Color('black'))
                self.display.blit(text, [150*index, 0])
                index += 1
        
        pygame.display.flip()

    def getAngleFromPoints(self):
        targetPos = self.targetGroup.sprite.rect.center
        vehiclePos = self.vehicleGroup.sprite.rect.center
        dx = targetPos[0] - vehiclePos[0]
        
        # Y-values on the screen get larger going down the screen, so the y needs to be inverted
        dy = vehiclePos[1] - targetPos[1]
        
        result = math.degrees(math.atan2(dy, dx))
        result -= self.vehicleGroup.sprite.nav.vehicleAngle
        if result <= -180:
            result += 360
        
        return result