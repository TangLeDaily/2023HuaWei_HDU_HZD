from utils import *

class Platform:
    def __init__(self, platformId, productId, position):
        self.platformId = platformId
        self.productId = productId
        self.product = None
        self.productSellWhat = productId if productId <= 7 else 0
        self.position = position
        self.produceTime = None
        self.rawmMterialHold = None
        self.bookHold = 0
        self.productComposition = {4: [1, 2],
                                   5: [1, 3],
                                   6: [2, 3],
                                   7: [4, 5, 6],
                                   8: [7],
                                   9: [1, 2, 3, 4, 5, 6, 7]}

    def sellIsReady(self, goods):
        if goods in self.productComposition.get(self.productId, []):
            if ((self.rawmMterialHold | self.bookHold) & (1 << goods)) == 0:
                return True
        return False

    def preBook(self, goods):
        self.bookHold |= (1 << goods)

    def unbook(self, goods):
        self.bookHold &= ~(1 << goods)
