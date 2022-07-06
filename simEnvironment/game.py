import pygame
import math
import os
from simEnvironment.globalResources import Point, WIDTH_BOARD, HEIGHT_BOARD
from simEnvironment.collidable import Collidable
from simEnvironment.mapManager import MapManager

# Choosing what goes into Viewing Data
commands = set()
commands.add('vehicle speed')
commands.add('vehicle angle')
commands.add('target direction')
commands.add('target distance')
commands.add('forward danger distance')
commands.add('backward danger distance')
commands.add('right danger distance')
commands.add('left danger distance')
# commands.add('left-forward danger distance')
# commands.add('right-forward danger distance')
# commands.add('position')
# commands.add('center x y')

# binary commands
commands.add('')


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
        self.vehicleToTarget = HEIGHT_BOARD
        
        
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
        self.vehicleToTarget = self.distanceToTarget()
        
    """
    GET STATE
    Collects viewing data about the environment
    """
    def getState(self, normalize=True):
        viewingData = []
        self.stateLabels.clear()
        vehicleCenter = self.vehicleGroup.sprite.rect.center
        maxDistance = math.sqrt(WIDTH_BOARD**2 + HEIGHT_BOARD**2)
        
        if 'vehicle speed' in commands:
            # Get Speed
            speed = self.vehicleGroup.sprite.nav.speed

            # Normalize
            if normalize:
                speed = (speed / (self.vehicleGroup.sprite.nav.maxSpeed * 2)) + 0.5
            
            # Add to data
            viewingData.append(speed)
            self.stateLabels.append('Speed:')
        
        if 'vehicle angle' in commands:
            # Get Angle
            vehicleAngle = self.vehicleGroup.sprite.nav.vehicleAngle
            
            # Normalize
            if normalize:
                vehicleAngle /= 360
            
            # Add to data
            viewingData.append(vehicleAngle)
            self.stateLabels.append('V_Angle:')
        
        if 'target direction' in commands:
            # Get Direction relative to vehicle angle
            targetDirection = self.getAngleFromPoints()

            # Normalize
            if normalize:
                targetDirection += 180
                targetDirection /= 360
                
            # Add to data
            viewingData.append(targetDirection)
            self.stateLabels.append('T_Direction:')
        
        if 'target distance' in commands:
            # Get Distance
            targetPosition = self.targetGroup.sprite.rect.center
            targetDistance = math.sqrt((targetPosition[0] - vehicleCenter[0])**2 + (targetPosition[1] - vehicleCenter[1])**2)
            
            # Normalize
            if normalize:
                # maxDistance = math.sqrt(WIDTH_BOARD**2 + HEIGHT_BOARD**2)
                targetDistance /= maxDistance
                
            # Add to data
            viewingData.append(targetDistance)
            self.stateLabels.append('T_Distance:')
            
        if 'forward danger distance' in commands:
            # Get Distance
            distance = self.shortestDistanceInDirection(vehicleCenter[0], vehicleCenter[1],
                                                        self.vehicleGroup.sprite.nav.vehicleAngle, 0)
            
            # Normalize
            if normalize:
                distance /= maxDistance
                
            # Add to data
            viewingData.append(distance)
            self.stateLabels.append('F_Danger:')
            
        if 'backward danger distance' in commands:
            # Get Distance
            distance = self.shortestDistanceInDirection(vehicleCenter[0], vehicleCenter[1],
                                                        self.vehicleGroup.sprite.nav.vehicleAngle, 180)
            
            # Normalize
            if normalize:
                distance /= maxDistance
                
            # Add to data
            viewingData.append(distance)
            self.stateLabels.append('B_Danger:')
            
        if 'right danger distance' in commands:
            # Get Distance
            distance = self.shortestDistanceInDirection(vehicleCenter[0], vehicleCenter[1],
                                                        self.vehicleGroup.sprite.nav.vehicleAngle, 270)
            
            # Normalize
            if normalize:
                distance /= maxDistance
                
            # Add to data
            viewingData.append(distance)
            self.stateLabels.append('R_Danger:')
            
        if 'left danger distance' in commands:
            # Get Distance
            distance = self.shortestDistanceInDirection(vehicleCenter[0], vehicleCenter[1],
                                                        self.vehicleGroup.sprite.nav.vehicleAngle, 90)
            
            # Normalize
            if normalize:
                distance /= maxDistance
                
            # Add to data
            viewingData.append(distance)
            self.stateLabels.append('L_Danger:')
            
        if 'left-forward danger distance' in commands:
            # Get Distance
            distance = self.shortestDistanceInDirection(vehicleCenter[0], vehicleCenter[1],
                                                        self.vehicleGroup.sprite.nav.vehicleAngle, 45)
            
            # Normalize
            if normalize:
                distance /= maxDistance
                
            # Add to data
            viewingData.append(distance)
            self.stateLabels.append('LF_Danger:')
            
        if 'right-forward danger distance' in commands:
            # Get Distance
            distance = self.shortestDistanceInDirection(vehicleCenter[0], vehicleCenter[1],
                                                        self.vehicleGroup.sprite.nav.vehicleAngle, -45)
            
            # Normalize
            if normalize:
                distance /= maxDistance
                
            # Add to data
            viewingData.append(distance)
            self.stateLabels.append('LF_Danger:')
            
        if 'position' in commands:
            x = self.vehicleGroup.sprite.rect.left
            y = self.vehicleGroup.sprite.rect.top
            
            if normalize:
                x /= WIDTH_BOARD
                y /= HEIGHT_BOARD
                
            viewingData.append(x)
            viewingData.append(y)
            self.stateLabels.append('X:')
            self.stateLabels.append('Y:')
            
        if 'center x y' in commands:
            x = vehicleCenter[0]
            y = vehicleCenter[1]
            
            if normalize:
                x /= WIDTH_BOARD
                y /= HEIGHT_BOARD
                
            viewingData.append(x)
            viewingData.append(y)
            self.stateLabels.append('X_C:')
            self.stateLabels.append('Y_C:')
            
            
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
            
            walls.extend(self.mapManager.createBorder())
            
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
            if self.frameCount > (1000 * (self.score + 1)):
                reward = -10
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
        wallCollisions = pygame.sprite.spritecollide(self.vehicleGroup.sprite, self.wallsList, False, pygame.sprite.collide_mask)
        if len(wallCollisions) > 0:
            # self.score += target.onCollision()
            reward = -100 * self.vehicleGroup.sprite.nav.speed
            gameOver = True

            return reward, gameOver, self.score
        
        endDistance = self.distanceToTarget()
        forwardProgress = self.vehicleToTarget - endDistance
        if forwardProgress > 0:
            reward = 5 * forwardProgress
            self.vehicleToTarget = endDistance
        # else:
        #     reward = forwardProgress - 1
        
        # Vehicle hit target
        targetCollisions = pygame.sprite.spritecollide(self.vehicleGroup.sprite, self.targetGroup, False, pygame.sprite.collide_mask)
        for target in targetCollisions:
            self.score += target.onCollision()
            reward += 1000
            self.vehicleToTarget = self.distanceToTarget()
        
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
        heldKeys = pygame.key.get_pressed()
        if heldKeys[pygame.K_UP]:
            action[0] = 1   # [1, 0, 0, -, -, -]
        elif heldKeys[pygame.K_DOWN]:
            action[1] = 1   # [0, 1, 0, -, -, -]
            
        if heldKeys[pygame.K_LEFT]:
            action[3] = 1   # [-, -, -, 1, 0, 0]
        elif heldKeys[pygame.K_RIGHT]:
            action[4] = 1   # [-, -, -, 0, 1, 0]
        
        return action
    
    def getOtherUserEvents(self):
        for event in pygame.event.get():
            # Need to check if the user has requested to close the window entirely
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
    
    def distanceToTarget(self):
        vehicleX = self.vehicleGroup.sprite.rect.centerx
        vehicleY = self.vehicleGroup.sprite.rect.centery

        targetX = self.targetGroup.sprite.rect.centerx
        targetY = self.targetGroup.sprite.rect.centery
        
        return math.sqrt((vehicleX - targetX)**2 + (vehicleY - targetY)**2)
                  
    """
    DRAW
    Draws everything to the display
    """
    def draw(self):
        self.display.fill(pygame.Color('green'))
        self.allSpritesList.draw(self.display)
        
        if self.playerDriven:
            viewingData = self.getState(normalize=False)
            index = 0
            
            for stat in viewingData:
                text = font.render(f'{self.stateLabels[index]} {stat:.2f}', True, pygame.Color('black'))
                self.display.blit(text, [150*(index%5), 20*int(index/5.0)])
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
    
    def shortestDistanceInDirection(self, startingX, startingY, vehicleFacingAngle, angleOffset):
        pass
        # Find endpoint in direction (size of line doesn't matter, just larger than the screen)
        magnitude = WIDTH_BOARD + HEIGHT_BOARD
        endingX = startingX + magnitude * math.cos(math.radians(vehicleFacingAngle + angleOffset))
        endingY = startingY - magnitude * math.sin(math.radians(vehicleFacingAngle + angleOffset))

        # Loop through walls to get clipline
        collisionPoints = []
        for wall in self.wallsList:
            clippedLine = wall.rect.clipline(startingX, startingY, endingX, endingY)
            if clippedLine:
                start, end = clippedLine
                collisionPoints.append(start)
                
        # Find distance for each point found
        distances = []
        for point in collisionPoints:
            x, y = point
            distance = math.sqrt((startingX - x)**2 + (startingY - y)**2)
            distances.append(distance)

        # Return smallest distance
        return min(distances)