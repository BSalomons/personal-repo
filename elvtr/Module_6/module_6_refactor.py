import pandas as pd
import numpy as np
from collections import namedtuple

"""
class Vaccinated takes a dataframe with:
 - a label, 
 - a Total affected column name, and 
 - a Vaccinated affected column name.
It calculates the unvaccinated affected. 
"""

CovidNums = namedtuple("CovidNums", "state vaccinated unvaccinated")

class Vaccinated():
    def __init__(self, df: pd.DataFrame, label: str, total_col: str, vacc_col: str):
        self._df = df
        self._label = df[label].tolist()
        self._total = df[total_col].tolist()
        self._vaccinated = df[vacc_col].tolist()

    @property
    def label(self, labels: list):
        self._label = labels

    @label.getter
    def label(self):
        return self._label

    @property
    def total(self, totals: list):
        self._total = np.array(totals)

    @total.getter
    def total(self):
        return self._total

    @property
    def vaccinated(self, vaccinated: list):
        self._vaccinated = np.array(vaccinated)

    @vaccinated.getter
    def vaccinated(self):
        return self._vaccinated

    def unvaccinated(self) -> list:
        return np.subtract(self.total, self.vaccinated)

    def as_namedtuple_list(self) -> list:
        ans = []
        for i in range(len(self.total)):
            entry = CovidNums(state=self.label[i], vaccinated=self.vaccinated[i], unvaccinated=self.unvaccinated()[i])
            ans.append(entry)
        return ans





