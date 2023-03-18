import math

buyPrice = {1: 3000,
             2: 4400,
             3: 5800,
             4: 15400,
             5: 17200,
             6: 19200,
             7: 76000}
sellPrice = {1: 6000,
              2: 7600,
              3: 9200,
              4: 22500,
              5: 25000,
              6: 27500,
              7: 105000}

def getTwoPositionDistance(position1, position2):
    return math.sqrt(pow((position1.x - position2.x), 2) + pow((position1.y - position2.y), 2))


def getWorthRatio(x, maxX, minRate):
    if x < maxX:
        return (1 - math.sqrt(1 - (1 - x / maxX) ** 2)) * (1 - minRate) + minRate
    else:
        return minRate

def getWorth(goodsId, time):
    return getWorthRatio(time, 9000, 0.8) * sellPrice.get(goodsId, 0) - buyPrice.get(goodsId)

def nearBorder(position):
    x = 50-position.x
    y = 50-position.y
    if x<3 or x>47 or y<3 or y>47:
        return True
    else:
        return False

def foot_point_of_point_to_segment(x0, y0, x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return x1, y1,True
    k = -((x1 - x0) * (x2 - x1) + (y1 - y0) * (y2 - y1)) / ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    xf = k * (x2 - x1) + x1
    yf = k * (y2 - y1) + y1
    flag = True
    if k < 0 or k > 1:
        flag = False
    return xf, yf, flag


def get_distance_from_point_to_line(x1, y1, x2, y2, x3, y3):

    A = y3 - y2
    B = x2 - x3
    C = (y2 - y3) * x2 + \
        (x3 - x2) * y2
    distance = abs(A * x1 + B * y1 + C) / (math.sqrt(A**2 + B**2))
    return distance

# if __name__ == "__main__":
#     print(get_distance_from_point_to_line(0,0,0,100,100,0))
#     print(foot_point_of_point_to_segment(0,0,0,100,100,0))

class Work:
    def __init__(self, buyPlatformOrinId, sellPlatformOrinId):
        self.buyPlatformOrinId = buyPlatformOrinId
        self.sellPlatformOrinId = sellPlatformOrinId
        self.alreadyBuy = False
        self.alreadySell = False

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y