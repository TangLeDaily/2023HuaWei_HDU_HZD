

class Order:
    def __init__(self, buy_bar_id: int, sell_bar_id: int):
        self.buy_bar_id = buy_bar_id    # which workbench to buy the goods
        self.sell_bar_id= sell_bar_id   # which workbench to sell the goods
        self.bought     = False         # whether the goods was bought
        self.sold       = False         # whether the goods was sold
    
    def complete(self):
        return self.bought and self.sold

