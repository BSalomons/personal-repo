import logging
from datetime import datetime
import pandas as pd
from pathlib import Path
from typing import Union, List
from trade import Trade
from TradeWrapper import TradeWrapper

"""
The Broker class does items related to a Brokerage firm, like:
  - Maintain a cash balance
  - record trades in a portfolio
  - tell us how many shares we can buy
  - reports opening and closing cash
"""
class Broker:
    def __init__(self, ticker: str, starting_bal: Union[float, int] = 10000):
        self.logger = logging.getLogger('StockProject.Broker')
        self._ticker = ticker
        self._df = self.read_prices()
        self._starting_bal = starting_bal
        self._cash = starting_bal
        self._trade_wrappers = []
        self.init_portfolio(starting_bal)

    def init_portfolio(self, starting_bal: Union[float, int] = None):
        """
        Empty out the trade list and set the cash to the starting balance
        :param starting_bal:
        :return:
        """
        self._cash = starting_bal or self._starting_bal
        self._trade_wrappers = []

    @property
    def ticker(self):
        return self._ticker

    @property
    def trades(self) -> List:
        all_trades = [t.trade for t in self._trade_wrappers] # Turn list of TradeWrappers into list of Trades
        return all_trades

    @property
    def trades_as_df(self) -> pd.DataFrame:
        df = pd.DataFrame(data=self.trades)
        return df

    @property
    def cash(self):
        return self._cash

    # methods involving the portfolio
    def add_tradeWrapper(self, trade_wrapper: TradeWrapper):
        """
        Reduce (or raise) cash by the amount of the stock purchase (or sale)
        Add the trade to the list of trades.
        :param trade_wrapper    wrapped trade object
        :return:
        """
        trade = trade_wrapper.trade
        self._cash = self._cash - trade.net_shares * trade.price - trade.commission
        self._trade_wrappers.append(trade_wrapper)

    def portfolio(self, report_all=False):
        """
        Return the portfolio as a dataframe.
        :param report_all: if True, report even if net shares are 0. If False, don't report if the net shares are 0.
        :return:
        """
        port_df = self.trades_as_df
        if port_df.empty:
            return port_df
        netted_df = port_df.groupby(port_df.ticker).sum()
        if report_all:
            return netted_df
        return netted_df[netted_df['net_shares'] != 0]

    def trade_report(self):
        for trade_no, trade_wrapper in enumerate(self._trade_wrappers, start=1):
            self.logger.info(f'{trade_no:3d}. {trade_wrapper}')

    def report(self):
        """
        Generate a report of our portfolio balances and final cash.
        :return:
        """
        df = self.portfolio()
        self.logger.info(f'Cash report\nStarting balance: ${self._starting_bal:.2f}\nEnding balance: ${self.cash_balance():.2f}')
        self.logger.info('Trades')
        self.trade_report()
        if len(df):
            df.drop(columns=['price', 'shares'], inplace=True)
            self.logger.info(f'Portfolio report\nPortfolio\n{df}\n')
        else:
            self.logger.info(f'Portfolio report\nEmpty portfolio\n')
        pass # TODO: Summarize the trade gains or losses with count, average, max loss, max gain
        pass # TODO: Summarize the percentage gain for this system


    def tickers(self) -> List:
        """
        Report the tickers
        :return: List of unique tickers.
        """
        return self.trades_as_df.ticker.unique().tolist()

    def cash_balance(self) -> float:
        return self._cash

    def is_flat(self) -> bool:
        """
        Look at the net portfolio
        :return: True iff net portfolio is empty.
        """
        net_df = self.portfolio(report_all=False)
        return len(net_df) == 0

    # methods involving the prices DB
    def row_count(self):
        return len(self._df)

    def closing_prices(self, closing_col_name: str = 'Close') -> pd.DataFrame:
        """
        return the closing prices as a ddtaframe.
        :param closing_col_name: column name to use to slice the closing prices, e.g., 'Adj Close'
        :return: dataframe of the requested column
        """
        return self._df[closing_col_name]

    def price_at_date(self, date: Union[datetime, str],  format: str = '%Y-%m-%d') -> pd.DataFrame:
        """

        :param date:
        :param format:   format of the date; see https://docs.python.org/3/library/datetime.html?highlight=strptime#strftime-and-strptime-behavior
        :return:
        """
        dt = date if isinstance(date, datetime) else datetime.strptime(date, format)
        try:
            row = self._df[self._df.index == dt]
            ans = (self.ticker, date, row['Close'][0], row['Adj Close'][0])
            return ans
        except IndexError:
            self.logger.warning(f'Could not find date {date}! Returning None.')
            return None

    def read_prices(self):
        raise NotImplementedError('must be implemented in subclass')

    def coerce_to_date(self, date_col: str = 'Date', format: str = '%Y-%m-%d'):
        """
        Coerce the date column to a string for the internal dataframe.
        :param date_col: string of the column name, default 'Date'
        :param format:   format of the date; see https://docs.python.org/3/library/datetime.html?highlight=strptime#strftime-and-strptime-behavior
        :return:
        """
        self._df[date_col] = pd.to_datetime(self._df[date_col], format=format)

    def set_index(self, index_col: str = 'Date'):
        """
        Set the index column for the internal dataframe.
        :param index_col: string of the column name, default 'Date'
        :return: None
        """
        self._df.set_index(keys=index_col, inplace=True)
        return

    def head(self, how_many: int = 5):
        """
        Print the first n records of the dataframe.

        :param how_many: how many to print
        :return: None
        """
        self.logger.info(self._df.head(how_many))

    def graph(self):
        """
        Display a graph of the prices with the system buys and sells.
        TODO: Add a graph for the technical indicators.
        :return:
        """
        pass # TODO: Put your code here!


class Static_Broker(Broker):
    def __init__(self, ticker: str):
        super().__init__(ticker)
        self.logger.debug('instantiating prices in Static_Broker')
        self.coerce_to_date('Date', format='%Y-%m-%d')
        self.set_index('Date')

    def read_prices(self):
        fn = f'{self.ticker}.CSV'
        p = Path(fn)
        if not p.is_file():
            self.logger.error(f'cannot find file {fn}.')

        ans = pd.read_csv(p)
        self.logger.debug(f'read {len(ans)} records from {fn}')
        return ans


