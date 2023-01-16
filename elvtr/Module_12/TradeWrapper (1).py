from datetime import datetime
from typing import Union
from trade import Trade

class TradeWrapper:
    def __init__(self, date: datetime, ticker: str, price: float, shares: Union[float, int], buy_or_sell: str = 'b',
                 open_or_close: str = 'o', commission: float = 0.0):
        self._date = date
        self._ticker = ticker.upper()
        self._price = price
        self._shares = shares
        self._b_s = buy_or_sell.lower()[0]
        self._o_c = open_or_close.lower()[0]
        self._commission = commission
        self._net_shares = shares if self.is_buy else (-1) * shares # so sell 10 shares makes _net_shares -10.
        self._trade = Trade(self.date, self.ticker, self.price, self._net_shares, self._b_s, self._o_c, self._net_shares, self._commission)

    @property
    def trade(self):
        return self._trade

    @property
    def date(self):
        return self._date

    @property
    def ticker(self):
        return self._ticker

    @property
    def price(self):
        return self._price

    @property
    def shares(self):
        return self._shares

    @property
    def is_buy(self):
        return self._b_s == 'b'

    @property
    def is_sell(self):
        return not self.is_buy

    @property
    def is_open(self):
        return self._o_c == 'o'

    @property
    def is_close(self):
        return not self.is_open

    @property
    def net_shares(self):
        return self._net_shares

    def __str__(self) -> str:
        b_s = 'bought' if self.is_buy else 'sold'
        o_c = 'open' if self.is_open else 'close'
        return  f'On {self.date}, {b_s} {self.shares} shares of {self.ticker} to {o_c}'
