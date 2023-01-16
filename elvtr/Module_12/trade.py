from collections import namedtuple

"""
The Trade class is simply a namedtuple that has the fields of a trade in it, like date, ticker, price, and shares.
We don't normally call it directly; instead, we use TradeWrapper.
b_s is buy/sell and is a single letter 'b' or 's'
o_c is open/close and is a single letter 'o' or 'c'
net_shares is the same as shares for buy. It's -1 * shares for a sell. (So Buy 100 shares IBM -> net_shares = 100. Sell 1 share IBM -> net_shares = -1
"""
# Just a namedtuple.
Trade = namedtuple("Trade", "date ticker price shares b_s o_c net_shares commission")
