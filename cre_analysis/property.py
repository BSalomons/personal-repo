import logging
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
from dateutil import relativedelta
from typing import Union, List

"""
Lands, Property and Premises Classes
Getting Fields down
"""

# Lands
class Lands:
  def __init__(self):
    self.logger = logging.getLogger('DiscounterCF.Lands')
    

# Property is the 
class Property:
  def __init__(self):
    self.logger = logging.getLogger('DiscountedCF.Property')
    self._acres
    self._rentableSF
    self._usableSF
    self._premises_total
    self._premisesSF
    self._



class Premises:
  def __init__(self):
    self.logger = logging.getLogger('DiscountedCF.Premises')
    self._unitsize
    self._unit_number
