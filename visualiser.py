#!/usr/bin/python

import pygame
from pygame.locals import *
from MindwaveDataPoints import *
from MindwaveDataPointReader import MindwaveDataPointReader

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1960, 1080))
pygame.display.set_caption('MindWave')

myfont = pygame.font.SysFont(None, 56)

class Point():
    pass

class Circle:
    def __init__(self, pos, colour, smoothingConstant=0.25):
        self.position = pos
        self.colour = colour
        self.level = 0.0
        self.prevLevel = 0.0
        self.smoothingConstant = smoothingConstant

    def update(self, level):
        self.prevLevel = self.level
        self.level = ((1-self.smoothingConstant) * self.prevLevel) + (self.smoothingConstant * level)

    def render(self, background):
        level = float(self.level)/100
        pygame.draw.circle(background, (0, 0, 0), self.position, 500, 1)
        pygame.draw.circle(background, self.colour, self.position, int(500*level), 0)


if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()

    # Get positions for the circles
    third = (screen.get_size()[0]/3, screen.get_size()[1]/2)
    secondThird = (2*screen.get_size()[0]/3, screen.get_size()[1]/2)

    # Create a circle for attention
    red = (255,0,0)
    attentionCircle = Circle(third, red)

    # Create a circle for meditation
    blue = (0, 255, 0)
    meditationCircle = Circle(secondThird, blue)

    lastMeditation = 0
    lastAttention = 0

    background = pygame.Surface(screen.get_size())

    while(True):
        dataPoint = mindwaveDataPointReader.readNextDataPoint()
        if (not dataPoint.__class__ is RawDataPoint):
            # Draw the background
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill((250, 250, 250))
            p = Point()
            if isinstance(dataPoint, MeditationDataPoint):
                #print "Meditation " , dataPoint.meditationValue
                p.meditation = int(dataPoint.meditationValue)
                lastMeditation = p.meditation
            elif isinstance(dataPoint, AttentionDataPoint):
                #print "Attetntion " , dataPoint.attentionValue
                p.attention = int(dataPoint.attentionValue)
                lastAttention = p.attention

            elif isinstance(dataPoint, EEGPowersDataPoint):
                #print "EEGPowers"
                p.delta = dataPoint.delta
                p.theta = dataPoint.theta
                p.lowAlpha = dataPoint.lowAlpha
                p.highAlpha = dataPoint.highAlpha
                p.lowBeta = dataPoint.lowBeta
                p.highBeta = dataPoint.highBeta
                p.lowGamma = dataPoint.lowGamma
                p.midGamma = dataPoint.midGamma
            elif isinstance(dataPoint, PoorSignalLevelDataPoint):
                #print "NoiseDataPoint" , dataPoint.amountOfNoise
                p.noise = int(dataPoint.amountOfNoise)
                # Draw the noise level if there is noise
                if p.noise > 0:
                    label = myfont.render("Noise: "+str(p.noise), 1, (0,0,0))
                    print "Noise:", p.noise
                    background.blit(label, (10, 10))

            meditationCircle.update(lastMeditation)
            attentionCircle.update(lastAttention)

            # Render the circles
            attentionCircle.render(background)
            meditationCircle.render(background)

            # Render everything!
            screen.blit(background, (0, 0))
            pygame.display.flip()
