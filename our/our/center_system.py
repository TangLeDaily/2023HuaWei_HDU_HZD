import sys

from car import Car
from platform import Platform
from utils import *



class CenterSystem:
    def __init__(self):
        self.cars = []
        self.platforms = []
        self.distance = None
        self.frame = -1
        self.maxDistance = None
        self.avgDistance = None
        # self.juli = None

        self.controlData = None

    def initControlData(self, controlData):
        self.controlData = controlData


    def getCenterPosition(self, i, j):
        x = j * 0.5 + 0.25
        y = (99 - i) * 0.5 + 0.25
        return Position(x, y)

    def getPlatformDistance(self, platformLen):
        self.distance = [[0.] * platformLen for _ in range(platformLen)]
        self.juli = [[[9999 for k in range(platformLen)] for j in range(platformLen)] for i in range(platformLen)]
        self.maxDistance = -9999
        sum = 0
        for i in range(platformLen):
            for j in range(platformLen):
                self.distance[i][j] = getTwoPositionDistance(self.platforms[i].position, self.platforms[j].position)
                self.maxDistance = max(self.maxDistance, self.distance[i][j])
                sum += self.distance[i][j]
        # for i in range(platformLen):
        #     for j in range(platformLen):
        #         for k in range(platformLen):
        #             p1 = self.platforms[i]
        #             p2 = self.platforms[j]
        #             p3 = self.platforms[k]
        #             _,_,flag = foot_point_of_point_to_segment(p1.position.x,
        #                                                       p1.position.y,
        #                                                       p2.position.x,
        #                                                       p2.position.y,
        #                                                       p3.position.x,
        #                                                       p3.position.y,
        #                                                       )
        #             if flag:
        #                 self.juli[i][j][k] = get_distance_from_point_to_line(p1.position.x,
        #                                                       p1.position.y,
        #                                                       p2.position.x,
        #                                                       p2.position.y,
        #                                                       p3.position.x,
        #                                                       p3.position.y,
        #                                                       )
        #             else:
        #                 self.juli[i][j][k] = 9999
        self.avgDistance = sum/(platformLen * platformLen)


    def inputOver(self):
        sys.stdout.write("OK")
        sys.stdout.flush()

    def getMapData(self):
        carId = 0
        platformId = 0
        for i in range(100):
            line = sys.stdin.readline().strip()
            for j in range(100):
                if line[j] == '.':
                    continue
                if line[j] == 'A':
                    car = Car(carId, 0, self.getCenterPosition(i, j))
                    car.setInit(initSpeed=self.controlData.get("initSpeed"),
                                toleranceToward=self.controlData.get("toleranceToward"),
                                towardSpeedAlpha=self.controlData.get("towardSpeedAlpha"),
                                towardSpeedBeta=self.controlData.get("towardSpeedBeta"),
                                boomTowardSpeedAlpha=self.controlData.get("boomTowardSpeedAlpha"),
                                boomTowardSpeedBeta=self.controlData.get("boomTowardSpeedBeta")
                                )
                    self.cars.append(car)
                    carId += 1
                else:
                    self.platforms.append(Platform(platformId, int(line[j]), self.getCenterPosition(i, j)))
                    platformId += 1
        self.getDataOver()
        self.getPlatformDistance(platformId)
        self.inputOver()

    def getFrameStartData(self):
        line = sys.stdin.readline()
        if line == '':
            return False
        frameStartData = line.split(' ')
        self.frame = int(frameStartData[0])
        return True

    def getPlatformsData(self):
        size = int(sys.stdin.readline().strip())
        for i in range(size):
            line = sys.stdin.readline().strip()
            lineData = line.split()
            self.platforms[i].position = Position(float(lineData[1]), float(lineData[2]))
            self.platforms[i].produceTime = int(lineData[3])
            self.platforms[i].rawmMterialHold = int(lineData[4])
            self.platforms[i].product = int(lineData[5])

    def getCarsData(self):
        for i in range(4):
            line = sys.stdin.readline().strip()
            lineList = line.split()
            self.cars[i].platformId = int(lineList[0])
            self.cars[i].goods = int(lineList[1])
            self.cars[i].timeRatio = float(lineList[2])
            self.cars[i].boomRatio = float(lineList[3])
            self.cars[i].palstance = float(lineList[4])
            self.cars[i].speed_x = float(lineList[5])
            self.cars[i].speed_y = float(lineList[6])
            self.cars[i].toward = float(lineList[7])
            self.cars[i].position.set(float(lineList[8]), float(lineList[9]))

    def getDataOver(self):
        line = sys.stdin.readline().strip()
        assert line == 'OK'

    def getGameData(self):
        if self.getFrameStartData():
            self.getPlatformsData()
            self.getCarsData()
            self.getDataOver()
            return True
        else:
            return False

    def beforeCenterComputerFunction(self):
        return

    def setTargetWork(self, buyPlatformId, sellPlatformId, car):
        car.nowWork = Work(buyPlatformId, sellPlatformId)
        self.platforms[sellPlatformId].preBook(self.platforms[buyPlatformId].productSellWhat)
        self.platforms[buyPlatformId].preBook(0)

    def setTheBestCommand(self, car):
        maxWeight = -9999
        buyPlatformId = -1
        sellPlatformId = -1
        for buyPlatform in self.platforms:
            if buyPlatform.product == 1 and buyPlatform.bookHold & 1 == 0:
                buyDistance = getTwoPositionDistance(car.position, buyPlatform.position)
                for sellPlatform in self.platforms:
                    if sellPlatform.sellIsReady(buyPlatform.productSellWhat):
                        sellDistance = self.distance[buyPlatform.platformId][sellPlatform.platformId]
                        near = nearBorder(sellPlatform.position)
                        nearDecri = 1
                        if near:
                            nearDecri = self.controlData.get("nearDecri")
                        # v0 = car.speed
                        # v1 = self.controlData.get("sumDistanceA") * v0 * 0.72
                        # weight = getWorth(buyPlatform.productSellWhat, (sellDistance / v1+self.controlData.get("sumDistanceB")) * 50) / ((buyDistance/v0+sellDistance/v1))

                        sumDistance = nearDecri * (buyDistance + sellDistance) * self.controlData.get("sumDistanceA") + self.controlData.get("sumDistanceB")
                        weightDistance = pow(self.avgDistance/sellDistance ,self.controlData.get("weightDistance"))
                        weight = weightDistance * getWorth(buyPlatform.productSellWhat, (sellDistance / self.controlData.get("sellDistanceA") + self.controlData.get("sellDistanceB")) * 50) / sumDistance
                        if weight > maxWeight:
                            maxWeight = weight
                            buyPlatformId = buyPlatform.platformId
                            sellPlatformId = sellPlatform.platformId
        if maxWeight == -9999:
            car.nowWork = None
            return
        else:
            self.setTargetWork(buyPlatformId, sellPlatformId, car)

    def findBetterCommand(self, car):
        nowWeoght = getWorth(car)
        maxWeight = -9999
        buyPlatformId = -1
        sellPlatformId = -1
        for buyPlatform in self.platforms:
            if buyPlatform.product == 1 and buyPlatform.bookHold & 1 == 0:
                buyDistance = getTwoPositionDistance(car.position, buyPlatform.position)
                for sellPlatform in self.platforms:
                    if sellPlatform.sellIsReady(buyPlatform.productSellWhat):
                        sellDistance = self.distance[buyPlatform.platformId][sellPlatform.platformId]
                        # v0 = car.speed
                        # v1 = self.controlData.get("sumDistanceA") * v0 * 0.72
                        # weight = getWorth(buyPlatform.productSellWhat, (sellDistance / v1+self.controlData.get("sumDistanceB")) * 50) / ((buyDistance/v0+sellDistance/v1))

                        sumDistance = (buyDistance + sellDistance) * self.controlData.get(
                            "sumDistanceA") + self.controlData.get("sumDistanceB")
                        # weightDistance = self.avgDistance/sellDistance * self.controlData.get("weightDistance")
                        weight = getWorth(buyPlatform.productSellWhat, (
                                    sellDistance / self.controlData.get("sellDistanceA") + self.controlData.get(
                                "sellDistanceB")) * 50) / sumDistance
                        if weight > maxWeight:
                            maxWeight = weight
                            buyPlatformId = buyPlatform.platformId
                            sellPlatformId = sellPlatform.platformId

        if maxWeight == -9999:
            car.nowWork = None
            return
        else:
            self.setTargetWork(buyPlatformId, sellPlatformId, car)

    def getNowWeight(self, car):
        shendistance = getTwoPositionDistance(car.position, car.targetPosition)
        worth = getWorth(car.goods, (shendistance / self.controlData.get("sellDistanceA") + self.controlData.get(
                                "sellDistanceB")) * 50) / shendistance * 1.2
        return worth

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
            # self.rotate = targetToward - self.toward

        if self.rotate == 0:
            self.speed = self.initSpeed
        else:
            self.speed = math.sqrt(getTwoPositionDistance(self.position,
                                                          self.targetPosition)) * self.towardSpeedAlpha + self.towardSpeedBeta
        if abs(targetToward - self.toward) > pi / 2:
            self.speed = 0

    def checkBoom(self,car):
        decriSpeed = False
        car_jilu = None
        waiting = False
        for carother in self.cars:
            if getTwoPositionDistance(carother.position, car.position) < self.controlData.get('boomDistance') and carother.id != car.id:
                waiting = True

                if car.goods<1:
                    if carother.goods<1:
                        decriSpeed |= False
                    else:
                        car_jilu = carother
                        decriSpeed |= True
                else:
                    if carother.goods<1:
                        decriSpeed |= False
                    else:
                        if car.goods>carother.goods:
                            # car_jilu = carother
                            # decriSpeed |= True
                            decriSpeed |= False
                        else:
                            car_jilu = carother
                            decriSpeed |= True
                            # if car.id>carother.id:
                            #     car_jilu = carother
                            #     decriSpeed |= True
                            # else:
                            #     decriSpeed |= False

        if decriSpeed:
            car.setSpeedAndRotateCarother(car_jilu)
            # car.speed = self.controlData.get('slowSpeed')
        else:
            if waiting:
                car.speed = self.controlData.get('slowSpeed')

    def CenterComputerFunction(self):
        for car in self.cars:
            if not car.alreadyHaveWork():
                self.setTheBestCommand(car)


    def afterCenterComputerFunction(self):
        return

    def setCarsAction(self):
        for car in self.cars:
            nowWork = car.nowWork
            if nowWork == None:
                car.targetPosition = Position(25, 25)
                continue
            if car.goods > 0:
                nowWork.alreadyBuy = True
                car.targetPosition = self.platforms[nowWork.sellPlatformOrinId].position
                car.doWhat = "sell"
            elif not nowWork.alreadyBuy:
                car.targetPosition = self.platforms[nowWork.buyPlatformOrinId].position
                car.doWhat = "buy" if self.frame < self.controlData.get('theTimeStopBuy') else None
                if self.frame > self.controlData.get('theTimeStopBuy'):
                    car.targetPosition = Position(25, 25)
            else:
                nowWork.alreadySell = True
                car.doWhat = None

            car.setSpeedAndRotate()
            self.checkBoom(car)
            car.setTheBuyOrSell(self.platforms)

    def putCommandToSys(self):
        sys.stdout.write(f"{self.frame}\n")
        for car in self.cars:
            sys.stdout.write(f"forward {car.id} {car.speed}\n")
            sys.stdout.write(f"rotate {car.id} {car.rotate}\n")
            if car.buy:
                sys.stdout.write(f"buy {car.id}\n")
            if car.sell:
                sys.stdout.write(f"sell {car.id}\n")
            if car.destroy:
                sys.stdout.write(f"destroy {car.id}\n")
        self.inputOver()