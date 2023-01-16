import logging
from datetime import datetime
from typing import Union

import pandas as pd

from TradeWrapper import TradeWrapper
from broker import Broker

"""
The TradingSystem class implements trading systems.
Known subclasses: BuyAndHoldSystem, SmaTrendSystem
  - You initialize it with a Broker (either dynamic or static)
  - Your subclass implements run(), which tells it when to buy and sell
  - tell us how many shares we can buy
  - reports opening and closing cash
"""
class TradingSystem:
    def __init__(self, broker: Broker):
        self.logger = logging.getLogger('StockProject.TradingSystem')
        self._broker = broker
        self._prices_df = pd.DataFrame(data=broker.closing_prices())

    def run(self):
        raise NotImplementedError('must be implemented in subclass')

    def buy_to_open(self, ticker: str, date: str, price: float, shares: Union[int, float]):
        trade1 = TradeWrapper(date=date, ticker=ticker, price=price, shares=shares, buy_or_sell='Buy',
                              open_or_close='open')
        self._broker.add_tradeWrapper(trade1)

    def sell_to_close(self, ticker: str, date: str, price: float, shares: Union[int, float]):
        trade1 = TradeWrapper(date=date, ticker=ticker, price=price, shares=shares, buy_or_sell='Sell',
                              open_or_close='close')
        self._broker.add_tradeWrapper(trade1)

    def sell_to_open(self, ticker: str, date: str, price: float, shares: Union[int, float]):
        raise NotImplementedError('must be implemented if you want to sell short') # TODO

    def buy_to_close(self, ticker: str, date: str, price: float, shares: Union[int, float]):
        raise NotImplementedError('must be implemented if you want to sell short') # TODO

    def add_indicator(self, indicator_type: str = 'SMA', indicator_period: int = 20):
        """
        Add an indicator to the dataframe
        :param indicator_type:
        :param indicator_period:
        :return:
        """
        indicator_type = indicator_type.upper()
        new_col = f'{indicator_type}_{indicator_period}' # Default is SMA_20
        if indicator_type == 'SMA':
            self._prices_df[new_col] = self._prices_df.rolling(window=indicator_period).mean()
        elif indicator_type == 'yourindicator':
            pass # TODO add your indicators here
        else:
            self.logger.warning(f'Cannot add an indicator type of {indicator_type}')
        return

    def close_positions(self, date: datetime, shares: Union[int, float]):
        """
        Close any open positions.
        :param date:
        :param shares:
        :return:
        """
        if self._broker.is_flat():
            return
        closes = self._broker.closing_prices()
        ticker, date, _, adj_close = self._broker.price_at_date(date=date)
        self.sell_to_close(ticker=ticker, date=date, price=adj_close, shares=shares)


class BuyAndHoldSystem(TradingSystem):
    def __init__(self, broker: Broker):
        super().__init__(broker)
        self.logger.debug('Starting buy-and-hold system.')

    def run(self):
        """
        Simply buy on the first day and sell on the last.
        :return:
        """
        closes = self._broker.closing_prices()
        shares = int(self._broker.cash_balance() / closes[0])
        ticker, date, _, adj_close = self._broker.price_at_date(closes.index[0])
        self.buy_to_open(ticker=ticker, date=date, price=adj_close, shares=shares)
        last = len(closes) - 1
        self.close_positions(date=closes.index[last], shares=shares)


class SmaTrendSystem(TradingSystem):
    def __init__(self, broker: Broker, sma_period: int = 20):
        super().__init__(broker)
        self.logger.debug('Starting SMA trend system.')
        indicator_type = 'SMA'

        self._indicator1 = f'{indicator_type}_{sma_period}' # Default is SMA_20
        self.add_indicator(indicator_type=indicator_type, indicator_period=sma_period)


    def run(self):
        """
        Simply buy on the first day and sell on the last.
        :return:
        """
        for row in self._prices_df.itertuples(name='Prices'):
            sma = getattr(row, self._indicator1) # Better than row.SMA_20

            if self._broker.is_flat():
                if row.Close > sma:
                    # We're flat and the Price crossed over SMA, so buy
                    ticker, date, _, _ = self._broker.price_at_date(row.Index)
                    shares = int(self._broker.cash_balance() / row.Close)
                    self.buy_to_open(ticker=ticker, date=date, price=row.Close, shares=shares)
            else:
                # We are long and will test to see if we should close the position
                if row.Close < sma:
                    # Price crossed under SMA, so sell
                    ticker, date, _, _ = self._broker.price_at_date(row.Index)
                    self.sell_to_close(ticker=ticker, date=date, price=row.Close, shares=shares)

        # After going through the DB, if we are not flat, then go flat.
        closes = self._broker.closing_prices()
        last = len(closes) - 1
        self.close_positions(date=closes.index[last], shares=shares)

# TODO: Add your own subclass of TradingSystem