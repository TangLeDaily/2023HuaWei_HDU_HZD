
from position import Position
import math

class Car:
    def __init__(self, id, position, toward):
        # 初始化可调控参数
        self.initSpeed = 6
        self.toleranceToward = 0.1



        self.id = id
        self.position = position
        self.toward = toward
        self.itemId = 0
        self.speed = self.initSpeed  # the speed we set for the robot
        self.rotate = 0  # the rotate we set for the robot

        self.targetPosition = Position(25, 42)  # the destination to go to
        self.doWhat = None  # 'buy' or 'sell' or None
        self.nowWorkDo = None  # the order to finish
        self.nowWorkId = None  # the order to finish
        self.nextWorkDo = None  # the order to do when the first order finished (not used yet)
        self.nextWorkId = None  # the order to do when the first order finished (not used yet)
        self.buy = False  # whether to buy the goods
        self.sell = False  # whether to sell the goods
        self.destroy = False  # whether to destroy the goods

        self.platformId = None
        self.timeRatio = None
        self.boomRatio = None
        self.palstance = None
        self.speed_x = None
        self.speed_y = None
    def setInit(self, initSpeed=6, toleranceToward = 0.1, towardSpeedAlpha = 2.8, towardSpeedBeta = -0.2):
        self.initSpeed = initSpeed
        self.toleranceToward = toleranceToward
        self.towardSpeedAlpha = towardSpeedAlpha
        self.towardSpeedBeta = towardSpeedAlpha

    def setCommand(self, command):
        """ status: the input string line """
        commandList = command.split()
        self.platformId = int(commandList[0])
        self.itemId = int(commandList[1])
        # sys.stderr.write(f"robot[{self.robot_id}.goods = {self.goods}]")
        self.timeRatio = float(commandList[2])
        self.boomRatio = float(commandList[3])
        self.palstance = float(commandList[4])
        self.speed_x = float(commandList[5])
        self.speed_y = float(commandList[6])
        self.toward = float(commandList[7])
        self.position.set(float(commandList[8]), float(commandList[9]))

    def heading(self, platforms) -> None:
        """ set the instructions. """

        targetToward = math.atan2(self.targetPosition.y - self.position.y,
                             self.targetPosition.x - self.position.x)  # the direction of the destination from the robot's stand
        if abs(targetToward - self.toward) > math.pi / 2:
            self.speed = 0
        else:
            if abs(targetToward - self.toward) < self.toleranceToward:  # stright to the detination, just go stright
                self.rotate = 0
            else:
                # make sure that the direction difference is in half a circle
                if abs(targetToward - self.toward) > math.pi:
                    if (targetToward + 2 * math.pi - self.toward) <= math.pi:
                        targetToward += 2 * math.pi
                    else:
                        targetToward -= 2 * math.pi
                # rotate in the right direction
                if targetToward > self.toward:
                    self.rotate = math.pi
                else:
                    self.rotate = -math.pi

            # v = sqrt(2ax)
            if self.rotate == 0:
                self.speed = self.initSpeed
            else:
                self.speed = math.sqrt(self.position.getThisPositionDistance(self.targetPosition)) * self.towardSpeedAlpha + self.towardSpeedBeta


        if self.doWhat == "buy" and self.platformId == self.nowWorkId:
            self.buy = True
            platforms[self.platformId].unbook(0)
        else:
            self.buy = False
        if self.todo == "sell" and self.bar_id == self.order.sell_bar_id:
            self.sell_ = True
            bars[self.bar_id].unbook(self.goods)
        else:
            self.sell_ = False

    def hasOrder(self) -> bool:
        """ to check if the robot has an unfinished order """
        if self.order is None and self.next_order is None:
            return False
        if self.order is not None and self.order.complete():
            if self.next_order is not None:
                self.order = self.next_order
                self.next_order = None
                return True
            else:
                self.order = None
                return False
        else:
            return True