from utils import *

class Car:
    def __init__(self, id, toward, position):
        self.initSpeed = 6
        self.toleranceToward = 0.1
        self.towardSpeedAlpha = 2.8
        self.towardSpeedBeta = -0.2
        self.boomTowardSpeedAlpha = 2.8
        self.boomTowardSpeedBeta = -0.2

        self.id = id
        self.position = position
        self.toward = toward
        self.goods = 0
        self.speed = self.initSpeed
        self.rotate = 0

        self.targetPosition = Position(25, 25)
        self.doWhat = None
        self.nowWork = None
        self.buy = False
        self.sell = False
        self.destroy = False

        self.platformId = None
        self.timeRatio = None
        self.boomRatio = None
        self.palstance = None
        self.speed_x = None
        self.speed_y = None

    def setInit(self, initSpeed=6, toleranceToward = 0.1, towardSpeedAlpha = 2.8, towardSpeedBeta = -0.2, boomTowardSpeedAlpha = 2.8, boomTowardSpeedBeta=-0.2):
        self.initSpeed = initSpeed
        self.toleranceToward = toleranceToward
        self.towardSpeedAlpha = towardSpeedAlpha
        self.towardSpeedBeta = towardSpeedBeta
        self.boomTowardSpeedBeta = boomTowardSpeedBeta
        self.boomTowardSpeedAlpha = boomTowardSpeedAlpha

    def setSpeedAndRotate(self):
        pi = math.pi
        targetToward = math.atan2(self.targetPosition.y - self.position.y,
                             self.targetPosition.x - self.position.x)
        if abs(targetToward - self.toward) < self.toleranceToward:
            self.rotate = 0
        else:
            if abs(targetToward - self.toward) > math.pi:
                if (targetToward + 2 * math.pi - self.toward) <= math.pi:
                    targetToward += 2 * math.pi
                else:
                    targetToward -= 2 * math.pi
            if targetToward > self.toward:
                self.rotate = math.pi
            else:
                self.rotate = -math.pi
            # self.rotate = targetToward #- self.toward

        if self.rotate == 0:
            self.speed = self.initSpeed
        else:
            self.speed = math.sqrt(getTwoPositionDistance(self.position, self.targetPosition))* self.towardSpeedAlpha + self.towardSpeedBeta
        if abs(targetToward - self.toward) > pi / 2:
            self.speed = 0

    def setSpeedAndRotateCarother(self, carother):
        pi = math.pi
        target = carother.position
        fuPosition = Position(2*self.position.x-target.x, 2*self.position.y-target.y)
        targetToward = math.atan2(fuPosition.y - self.position.y,
                                  fuPosition.x - self.position.x)
        if abs(targetToward - self.toward) < self.toleranceToward:
            self.rotate = 0
        else:
            if abs(targetToward - self.toward) > math.pi:
                if (targetToward + 2 * math.pi - self.toward) <= math.pi:
                    targetToward += 2 * math.pi
                else:
                    targetToward -= 2 * math.pi
            if targetToward > self.toward:
                self.rotate = math.pi
            else:
                self.rotate = -math.pi
            # self.rotate = targetToward - self.toward
        if self.rotate == 0:
            self.speed = self.initSpeed
        else:
            self.speed = math.sqrt(getTwoPositionDistance(self.position,
                                                          self.targetPosition)) * self.boomTowardSpeedAlpha + self.boomTowardSpeedBeta
        # if abs(targetToward - self.toward) > pi / 2:
        #     self.speed = 0


    def setTheBuyOrSell(self, platforms):
        if self.doWhat == "buy" and self.platformId == self.nowWork.buyPlatformOrinId:
            self.buy = True
            platforms[self.platformId].unbook(0)
        else:
            self.buy = False
        if self.doWhat == "sell" and self.platformId == self.nowWork.sellPlatformOrinId:
            self.sell = True
            platforms[self.platformId].unbook(self.goods)
        else:
            self.sell = False

    def alreadyHaveWork(self):
        if self.nowWork is None:
            return False
        if self.nowWork is not None and self.nowWork.alreadyBuy and self.nowWork.alreadySell:
            self.nowWork = None
            return False
        else:
            return True