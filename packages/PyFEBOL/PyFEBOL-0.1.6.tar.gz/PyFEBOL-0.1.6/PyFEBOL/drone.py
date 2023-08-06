'''
drone.py

Cedrick Argueta
cdrckrgt@stanford.edu

the drone and its movement
'''
import numpy as np

class Drone(object):
    def __init__(self, x, y, heading, maxStep, sensor, searchdomain):
        self.x = x
        self.y = y
        self.heading = heading
        self.maxStep = maxStep
        self.sensor = sensor
        self.searchdomain = searchdomain

    def getPose(self):
        return self.x, self.y, self.heading

    def getNewPose(self, action):
        newX = self.x + action[0]
        newY = self.y + action[1]
        newHeading = (self.heading + action[2]) % 360. # ensuring that heading remains within 360 degrees
        return newX, newY, newHeading

    def act(self, action):
        newX, newY, newHeading = self.getNewPose(Action)
        # make sure we stay within bounds
        newX, newY = np.clip([newX, newY], 0, self.searchdomain.length)
        self.x, self.y, self.heading = newX, newY, newHeading

    def observe(self, searchdomain):
        return self.sensor.observe(searchdomain.getTheta(), self.getPose())

if __name__ == '__main__':
    pass 
