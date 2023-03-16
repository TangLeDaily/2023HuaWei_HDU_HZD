import typing
import math
import sys

from order import Order
from utils import Position, dist, pi

class Robot:
    def __init__(self, robot_id: int, x: float, y: float, toward: float):
        self.robot_id   = robot_id          # unique id range[0,3]
        self.pos        = Position(x, y)    # the position of the robot
        self.toward     = toward            # the direction of the robot [-PI, PI]
        self.goods      = 0                 # the goods carried by the robot, 0 stands for no goods

        # order
        self.order      = None  # the order to finish
        self.next_order = None  # the order to do when the first order finished (not used yet)

        # destination
        self.destination= Position(25, 42)  # the destination to go to
        self.todo       = None  # 'buy' or 'sell' or None

        # instruct
        self.speed_     = 5.5     # the speed we set for the robot
        self.rotate_    = 0     # the rotate we set for the robot
        self.buy_       = False # whether to buy the goods
        self.sell_      = False # whether to sell the goods
        self.destroy_   = False # whether to destroy the goods

    def updateStatus(self, status: str):
        """ status: the input string line """
        status_list = status.split()
        self.bar_id      = int(status_list[0])
        self.goods       = int(status_list[1])
        # sys.stderr.write(f"robot[{self.robot_id}.goods = {self.goods}]")
        self.time_lambda = float(status_list[2])
        self.boom_lambda = float(status_list[3])
        self.omega       = float(status_list[4])
        self.speed_x     = float(status_list[5])
        self.speed_y     = float(status_list[6])
        self.toward      = float(status_list[7])
        x   = float(status_list[8])
        y   = float(status_list[9])
        self.pos.update(x, y)

    def heading(self, bars) -> None:
        """ set the instructions. """
        
        toward_ = math.atan2(self.destination.y - self.pos.y, self.destination.x - self.pos.x)  # the direction of the destination from the robot's stand
        if abs(toward_ - self.toward) < 0.1:    # stright to the detination, just go stright
            self.rotate_ = 0
        else: 
            # make sure that the direction difference is in half a circle
            if abs(toward_ - self.toward) > pi:
                if (toward_ + 2 * pi - self.toward) <= pi:
                    toward_ += 2 * pi
                else:
                    toward_ -= 2 * pi
            # rotate in the right direction
            self.rotate_ = pi if toward_ - self.toward > 0 else -pi
        
        # v = sqrt(2ax)
        self.speed_ = math.sqrt(dist(self.pos, self.destination)) * 2.8 - 0.2 if self.rotate_ != 0 else 5.5

        if abs(toward_ - self.toward) > pi / 2:
            self.speed_ = 0
        
        if self.todo == "buy" and self.bar_id == self.order.buy_bar_id:
            self.buy_ = True
            bars[self.bar_id].unbook(0)
        else:
            self.buy_ = False
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

