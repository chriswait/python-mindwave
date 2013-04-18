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

if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()

    while(True):
        points = []
        while (len(points)<4):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (not dataPoint.__class__ is RawDataPoint):
                points.append(dataPoint)

        p = Point()

        for point in points:

            if isinstance(point, MeditationDataPoint):
                #print "Meditation " , point.meditationValue
                p.meditation = int(point.meditationValue)
            elif isinstance(point, AttentionDataPoint):
                #print "Attetntion " , point.attentionValue
                p.attention = int(point.attentionValue)
            elif isinstance(point, EEGPowersDataPoint):
                #print "EEGPowers"
                p.delta = point.delta
                p.theta = point.theta
                p.lowAlpha = point.lowAlpha
                p.highAlpha = point.highAlpha
                p.lowBeta = point.lowBeta
                p.highBeta = point.highBeta
                p.lowGamma = point.lowGamma
                p.midGamma = point.midGamma
            elif isinstance(point, PoorSignalLevelDataPoint):
                #print "NoiseDataPoint" , point.amountOfNoise
                p.noise = int(point.amountOfNoise)

        # Draw the background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))

        # Get positions for the circles
        third = (screen.get_size()[0]/3, screen.get_size()[1]/2)
        secondThird = (2*screen.get_size()[0]/3, screen.get_size()[1]/2)

        # Draw a circle for attention
        attention = float(p.attention)/100
        pygame.draw.circle(background, (0, 0, 0), third, 500, 1)
        pygame.draw.circle(background, (255, 0, 0), third, int(500*attention), 0)

        # Draw a circle for meditation
        meditation = float(p.meditation)/100
        pygame.draw.circle(background, (0, 0, 0), secondThird, 500, 1)
        pygame.draw.circle(background, (0, 255, 0), secondThird, int(500*meditation), 0)

        # Draw the noise level if there is noise
        if p.noise > 0:
            label = myfont.render("Noise: "+str(p.noise), 1, (0,0,0))
            print "Noise:", p.noise
            background.blit(label, (10, 10))

        # Render everything!
        screen.blit(background, (0, 0))
        pygame.display.flip()


