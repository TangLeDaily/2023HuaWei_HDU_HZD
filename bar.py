

from utils import Position

# what goods the workbenches need (not used yet)
buys = {4: [1,2],
        5: [1,3],
        6: [2,3],
        7: [4,5,6],
        8: [7],
        9: [1,2,3,4,5,6,7]}

class Bar:
    """ workbench: Should I rename `bar` to `workbench` ? """
    def __init__(self, bar_id: int, bar_type: int, x: float, y: float):
        self.bar_id     = bar_id        # unique id [0, 49]
        self.bar_type   = bar_type      # type [1, 9]
        self.pos        = Position(x, y)# the position 
        self.book_mask = 0

    def updateStatus(self, status: str):
        """ update status from stdin """
        digits = status.split()
        assert int(digits[0])   == self.bar_type
        assert float(digits[1]) == self.pos.x
        assert float(digits[2]) == self.pos.y
        self.remaining   = int(digits[3])
        self.buy_mask    = int(digits[4])
        self.product     = bool(int(digits[5]))  # if there is a product to sell
        # if not self.product:
        #     self.book_mask &= ~1
        # self.book_mask &= ~self.buy_mask

    def buys(self):
        return buys.get(self.bar_type, [])
    def sells(self):
        return self.bar_type if self.bar_type <= 7 else 0
    
    def readyToBuy(self) -> bool:
        return self.book_mask & 1 == 0
    def readyToSell(self, goods: int) -> bool:
        return ((self.buy_mask | self.book_mask) & (1 << goods)) == 0 and goods in self.buys()
    def preBook(self, goods: int) -> None:
        self.book_mask |= (1 << goods)
    def unbook(self, goods: int) -> None:
        self.book_mask &= ~(1 << goods)
    @staticmethod
    def whoSells(self, goods_id):
        assert 1 <= goods_id <= 7
        return goods_id
    
    @staticmethod
    def whoBuys(self, goods_id):
        return [bar for bar, bar_buys in buys.items() if goods_id in bar_buys]