import sys
from math import sqrt

from robot import Robot
from bar import Bar
from order import Order
from instruct import Instruct
from utils import dist, pi, Position, profit

readline = sys.stdin.readline

class ControlCenter:
    def __init__(self) -> None:
        self.robots = []    # robots list
        self.bars   = []    # workbenches list
        self.instruct = Instruct([])    # send the instructions

    def readMaps(self):
        """ read the maps from stdin. """
        # rand the map data to an 2d array `string_maps`
        string_maps = []
        for i in range(100):
            line = sys.stdin.readline().strip()
            string_maps.append(line)
        line = sys.stdin.readline().strip() # last line should be `OK`
        assert line == "OK"

        # record each robot and each workbench
        for i in range(100):
            for j in range(100):
                if string_maps[i][j] == '.':
                    continue
                x = j * 0.5 + 0.25
                y = (99 - i) * 0.5 + 0.25
                if string_maps[i][j] == 'A':
                    robot = Robot(len(self.robots), x, y, 0)
                    self.robots.append(robot)
                else:
                    bar_type = int(string_maps[i][j])
                    bar = Bar(len(self.bars), bar_type, x, y)
                    self.bars.append(bar)
        self.instruct.robots = self.robots
        self.num_bars = len(self.bars)

        # self.dist stored the distance between any two workbenches
        self.dist = [[100.] * self.num_bars for _ in range(self.num_bars)]
        for i in range(self.num_bars):
            for j in range(self.num_bars):
                distance = dist(self.bars[i].pos, self.bars[j].pos)
                self.dist[i][j] = distance

        # tell the game that we are ready
        sys.stdout.write("OK")
        sys.stdout.flush()

    def readFrameID_money(self) -> bool:
        """ read the first line data: frame ID and money we have now. """
        line = sys.stdin.readline()
        if not line:
            return False
        parts = line.split(' ')
        self.frame_id = int(parts[0])
        self.money = int(parts[1])
        return True

    def readBarsStatus(self):
        """ read status of each workbench """
        num_bars = int(readline().strip())
        assert num_bars == self.num_bars
        for i in range(num_bars):
            line = readline().strip()
            self.bars[i].updateStatus(line)

    def readRobotStatus(self):
        """ read status of each robot """
        for i in range(4):
            status = readline().strip()
            self.robots[i].updateStatus(status)
        line = readline().strip()
        assert line == 'OK'

    def formOrders(self):
        """ generate a list of orders for the robot """
        # @TODO
        pass

    def getOrders(self):
        """ get an order for each robot """
        for robot in self.robots:
            if not robot.hasOrder():
                self.getOrder(robot)
    
    def getOrder(self, robot: Robot) -> None:
        """ get an order for the specific robot """
        """ it shows an stupid way to get order, NEED BETTER WAYS """
        choices = []
        for buy_bar in self.bars:
          if buy_bar.product and buy_bar.readyToBuy():
            dist1 = dist(robot.pos, buy_bar.pos)
            for sell_bar in self.bars:
              if sell_bar.readyToSell(buy_bar.sells()):
                  dist2 = self.dist[buy_bar.bar_id][sell_bar.bar_id]
                  distance = dist1 + dist2 + 8
                  weight = profit(buy_bar.sells(), (dist2 / 6 + 0.6) * 50) / distance
                  choices.append((buy_bar.bar_id, sell_bar.bar_id, weight))
        choices.sort(key=lambda x: x[2], reverse=True)
        if len(choices) == 0:
            robot.order = None
            return
        choice = choices[0]
        buy_bar_id, sell_bar_id, _ = choice
        self.bars[sell_bar_id].preBook(self.bars[buy_bar_id].sells())
        self.bars[buy_bar_id].preBook(0)
        robot.order = Order(buy_bar_id, sell_bar_id)

    def navigate(self):
        """  """
        for robot in self.robots:
            # get the destination: go to buy bar or go to sell bar
            order = robot.order
            if order == None:
                robot.destination = Position(25, 25)
                continue
            if robot.goods > 0: # robot carry the right goods, just sell it
                assert robot.goods == self.bars[order.buy_bar_id].bar_type
                order.bought = True
                robot.destination = self.bars[order.sell_bar_id].pos
                robot.todo = "sell"
            elif order.bought == True:  # finish the order
                order.sold = True
                robot.todo = None
            else:   # go to buy the goods
                robot.destination = self.bars[order.buy_bar_id].pos
                # last 5 seconds, don't buy anything
                robot.todo = "buy" if self.frame_id < 8840 else None
                if self.frame_id > 8840:
                    robot.destination = Position(0,0)
            # set the speed and roration and buy or sell parameters for the robot
            robot.heading(self.bars)

    def sendInstruct(self):
        self.instruct.send(self.frame_id)   # send instructions to the game
    