import math


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y

    def getTwoPositionDistance(self, position1, position2):
        return math.sqrt(pow((position1.x - position2.x), 2) + pow((position1.y - position2.y), 2))

    def getThisPositionDistance(self, position):
        return self.getTwoPositionDistance(self, position)
