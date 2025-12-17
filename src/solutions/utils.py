from typing import NamedTuple


class Item(NamedTuple):
    w: float                 # weight w_{ik}
    buy_price: float         # p_{ik}^{buy}
    sell_price: float        # p_{ik}^{sell}
    
class Merchandise(NamedTuple):
    i: int                   # port where it was bought
    k: int                   # merchandise index at that port
    w: float                 # merchandise weight
    buy_price: float         # p_{ik}^{buy}