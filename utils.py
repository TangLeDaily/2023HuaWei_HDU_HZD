import math
import random

pi = math.pi    # 3.1415926

class Position:
    """ define a position class """
    def __init__(self, x: float, y: float):
        self.x  = x
        self.y  = y

    def update(self, x: float, y: float):
        self.x  = x
        self.y  = y

def dist(a: Position, b: Position) -> float:
    """ return the distance between a and b. """
    delta_x = a.x - b.x
    delta_y = a.y - b.y
    return math.sqrt(delta_x * delta_x + delta_y * delta_y)

def discont(x: float, maxX: int, minRate: float) -> float:
    if x < maxX:
        return (1 - math.sqrt(1 - (1 - x / maxX) ** 2)) * (1 - minRate) + minRate
    else:
        return minRate
def profit(goods: int, time: float)-> float:
    """ the profit we can get to sell the goods. """
    buy_price = {1: 3000,
                 2: 4400,
                 3: 5800,
                 4: 15400,
                 5: 17200,
                 6: 19200,
                 7: 76000}
    sell_price = {1: 6000,
                  2: 7600,
                  3: 9200,
                  4: 22500,
                  5: 25000,
                  6: 27500,
                  7: 105000}
    def time_lambda(time: float) -> float:
        return discont(time, 9000, 0.8)
    return time_lambda(time) * sell_price.get(goods, 0) - buy_price.get(goods, 0)