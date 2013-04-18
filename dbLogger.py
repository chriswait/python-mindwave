import sys
import time
import lightblue as bluetooth
from MindwaveDataPoints import *
from MindwaveDataPointReader import MindwaveDataPointReader
import urllib2

user = sys.argv[1]
activity = sys.argv[2]

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

        baseURL = "http://optimusprime.local/cgi-bin/brain.py"
        url = baseURL+'?'
        fields = ['noise', 'meditation', 'attention' , 'delta', 'theta', 'low_alpha', 'high_alpha', 'low_beta', 'high_beta', 'low_gamma', 'high_gamma', 'time', 'user', 'activity']
        values = [p.noise, p.meditation, p.attention, p.delta, p.theta, p.lowAlpha, p.highAlpha, p.lowBeta, p.highBeta, p.lowGamma, p.midGamma, int(time.time()*1000), user, activity]
        formItems = []
        for field,value in zip(fields,values):
            formItem = str(field)+"="+str(value)
            formItems.append(formItem)
        url += "&".join(formItems)
        response = urllib2.urlopen(url).read()
     #   print response
        if response.strip() != "1":
            print "Failed"
