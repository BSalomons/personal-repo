import logging

from broker import Static_Broker
from tradingSystem import BuyAndHoldSystem, SmaTrendSystem

logger = logging.getLogger('StockProject.main')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.debug('Starting!')
b = Static_Broker('TSLA')

# Run 1: Buy and hold
s = BuyAndHoldSystem(broker=b)
s.run()
b.report()

# Run 2: SMA
b.init_portfolio() # set back to initial
s = SmaTrendSystem(broker=b, sma_period=50)
s.run()
b.report()

# Run 3: Your own system
b.init_portfolio() # set back to initial
# TODO: put your call here

logger.info('Done.')