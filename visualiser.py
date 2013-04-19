#!/usr/bin/python

import pygame
import random
from pygame.locals import *
from MindwaveDataPoints import *
from MindwaveDataPointReader import MindwaveDataPointReader

#screenSize = (1960, 1080)
screenSize = (3920, 1080)

class Point:
    def __init__(self):
        self.meditation = 0
        self.attention = 0
        self.noise = 0

        self.delta = 0
        self.theta = 0
        self.lowAlpha = 0
        self.highAlpha = 0
        self.lowBeta = 0
        self.highBeta = 0
        self.lowGamma = 0
        self.midGamma = 0

    def process(self, dataPoint):
        if isinstance(dataPoint, MeditationDataPoint):
            self.meditation = int(dataPoint.meditationValue)
        elif isinstance(dataPoint, AttentionDataPoint):
            self.attention = int(dataPoint.attentionValue)
        elif isinstance(dataPoint, EEGPowersDataPoint):
            #print "EEGPowers"
            self.delta = dataPoint.delta
            self.theta = dataPoint.theta
            self.lowAlpha = dataPoint.lowAlpha
            self.highAlpha = dataPoint.highAlpha
            self.lowBeta = dataPoint.lowBeta
            self.highBeta = dataPoint.highBeta
            self.lowGamma = dataPoint.lowGamma
            self.midGamma = dataPoint.midGamma
        elif isinstance(dataPoint, PoorSignalLevelDataPoint):
            self.noise = int(dataPoint.amountOfNoise)

class Circle:
    def __init__(self, pos, colour, smoothingConstant=0.25):
        self.position = pos
        self.colour = colour
        self.level = 0.0
        self.prevLevel = 0.0
        self.smoothingConstant = smoothingConstant

    def update(self, point):
        level = self.getLevel(point)
        if level:
            self.prevLevel = self.level
            self.level = ((1-self.smoothingConstant) * self.prevLevel) + (self.smoothingConstant * level)

    def render(self, background):
        level = float(self.level)/100
        pygame.draw.circle(background, (0, 0, 0), self.position, screenSize[0]/4, 1)
        pygame.draw.circle(background, self.colour, self.position, int((screenSize[0]/4)*level), 0)

class MeditationCircle(Circle):
    def getLevel(self, point):
        if hasattr(point, 'meditation'):
            return point.meditation

class AttentionCircle(Circle):
    def getLevel(self, point):
        if hasattr(point, 'attention'):
            return point.attention

class NoiseIndicator:
    def __init__(self,fontSize):
        self.myfont = pygame.font.SysFont(None, fontSize)
        self.noise = 0

    def update(self, point):
        if hasattr(point, 'noise'):
            self.noise = point.noise

    def render(self, background):
        # Draw the noise level if there is noise
        if self.noise > 0:
            label = self.myfont.render("Noise: "+str(self.noise), 1, (0,0,0))
            print "Noise:", self.noise
            background.blit(label, (10, 10))

class GridView:
    def __init__(self, frame):
        self.boxWidth = 30
        self.boxHeight = 30
        self.numWBoxes = frame.width / self.boxWidth
        self.numHBoxes = frame.height / self.boxHeight
        self.grid = self.numHBoxes * [[0]*self.numWBoxes]
        self.colours = self.getColours()
        self.level = 0
        self.prevLevel = 0
        self.smoothingConstant = 0.25
        self.threshold = 60
        self.newPath()
        self.frame = frame

    def update(self, point):
        self.prevLevel = self.getLevel(point)
        self.level = ((1-self.smoothingConstant) * self.prevLevel) + (self.smoothingConstant * point.meditation)

        numUpdates = abs(int((self.level - self.threshold) / 10))
        [self.updatePath() for i in range(numUpdates)]

    def newPath(self):
        wMiddle = self.numWBoxes/2
        hMiddle = self.numHBoxes/2
        self.path = [(wMiddle, hMiddle)]

    def updatePath(self):
        if self.level > self.threshold:
            foundCoord = 0
            while foundCoord < 10:
                lastItem = self.path[-1]
                direction = random.randrange(9)
                xDiff = (direction % 3) - 1
                yDiff = int(direction / 3) -1
                newCoord = (lastItem[0] + xDiff, lastItem[1] + yDiff)
                foundCoord +=1
                if newCoord not in self.path and self.inRange(newCoord):
                    self.path.append(newCoord)
                    return
            if len(self.path)>1:
                self.path.pop()
                self.updatePath()
        elif len(self.path)>1:
            self.path.pop()

    def inRange(self, newCoord):
        #return newCoord[0] >= 0 and newCoord[0] < self.numWBoxes and newCoord[1] >= 0 and newCoord[1] < self.numHBoxes:
        return newCoord[0] in range(self.numWBoxes) and newCoord[1] in range(self.numHBoxes)
        #return self.grid[newCoord[0]][newCoord[1]] != None

    def render(self, background):
        for (i, j) in self.path:
            n = i + j
            #n = int(self.level / 5)
            colour = self.colours[n % 5]
            x = self.frame.x+i*self.boxWidth
            y = self.frame.y+j*self.boxHeight
            #print "Box:", (x,y,self.boxWidth,self.boxHeight)
            if self.level < 60:
                pygame.draw.rect(background, (100,100,100), (x,y,self.boxWidth,self.boxHeight), 0)
            else:
                pygame.draw.rect(background, colour, (x,y,self.boxWidth,self.boxHeight), 0)

class MeditationGrid(GridView):
    def getLevel(self, point):
        if hasattr(point, "meditation"):
            return point.meditation
    def getColours(self):
        return [(207,240,158), (168,219,168), (121,189,154), (59,134,134), (11,72,107)]


class AttentionGrid(GridView):
    def getLevel(self, point):
        if hasattr(point, "attention"):
            return point.attention
    def getColours(self):
        return [(253,236,44), (255,198,25), (252,151,0), (255,102,0), (255,0,0)]

class Frame:
    def __init__(self):
        self.width = screenSize[0]/2
        self.height = screenSize[1]

if __name__ == '__main__':
    # Setup pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('MindWave')

    # Setup mindwave
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    p = Point()

    # Get positions for the circles
    third = (screen.get_size()[0]/4, screen.get_size()[1]/2)
    secondThird = (3*screen.get_size()[0]/4, screen.get_size()[1]/2)

    # Create a circle for attention
    red = (250,105,0)
    attentionCircle = AttentionCircle(third, red)

    # Create a circle for meditation
    blue = (105,210,231)
    meditationCircle = MeditationCircle(secondThird, blue)

    # Create noise indicator in the top left
    fontSize = 56
    noiseIndicator = NoiseIndicator(fontSize)

    # Set up the UI elements
    #ui = [attentionCircle, meditationCircle, noiseIndicator]

    frame = Frame()
    frame.x = 0
    frame.y = 0

    atGrid = AttentionGrid(frame)

    frame2 = Frame()
    frame2.x = frame.width
    frame2.y = 0

    medGrid = MeditationGrid(frame2)

    ui = [attentionCircle, meditationCircle, atGrid,medGrid, noiseIndicator]

    # Set up frame rate counter
    fps = 30
    lastRendered = pygame.time.get_ticks()

    # Main loop
    while(True):
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();
        dataPoint = mindwaveDataPointReader.readNextDataPoint()
        if (dataPoint.__class__ is RawDataPoint):
            continue
        p.process(dataPoint)

        for element in ui:
            element.update(p)

        # Limit the frame rate
        timeNow = pygame.time.get_ticks()
        if timeNow > (lastRendered+(1000/fps)):

            # Draw the background
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill((250, 250, 250))

            # Render the circles
            for element in ui:
                element.render(background)
            lastRendered = timeNow

            # Blit everything!
            screen.blit(background, (0, 0))
            pygame.display.flip()
