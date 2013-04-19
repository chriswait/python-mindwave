#!/usr/bin/python

import pygame
from pygame.locals import *
from MindwaveDataPoints import *
from MindwaveDataPointReader import MindwaveDataPointReader

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
        if (not dataPoint.__class__ is RawDataPoint):
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
        pygame.draw.circle(background, (0, 0, 0), self.position, 500, 1)
        pygame.draw.circle(background, self.colour, self.position, int(500*level), 0)

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
        if noise > 0:
            label = self.myfont.render("Noise: "+str(self.noise), 1, (0,0,0))
            print "Noise:", self.noise
            background.blit(label, (10, 10))


if __name__ == '__main__':
    # Setup pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1960, 1080))
    pygame.display.set_caption('MindWave')

    # Setup mindwave
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    p = Point()

    # Get positions for the circles
    third = (screen.get_size()[0]/3, screen.get_size()[1]/2)
    secondThird = (2*screen.get_size()[0]/3, screen.get_size()[1]/2)

    # Create a circle for attention
    red = (255,0,0)
    attentionCircle = AttentionCircle(third, red)

    # Create a circle for meditation
    blue = (0, 255, 0)
    meditationCircle = MeditationCircle(secondThird, blue)

    # Create noise indicator in the top left
    fontSize = 56
    noiseIndicator = NoiseIndicator(fontSize)

    # Set up the UI elements
    ui = [attentionCircle, meditationCircle, noiseIndicator]

    # Set up frame rate counter
    fps = 30
    lastRendered = pygame.time.get_ticks()

    # Main loop
    while(True):
        dataPoint = mindwaveDataPointReader.readNextDataPoint()
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
