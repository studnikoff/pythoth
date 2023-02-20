"""
Formatter Strategy Pattern
"""
from abc import ABC, abstractmethod
from copy import deepcopy

import pandas as pd

from .errors import StrategyError


class Strategy(ABC):
    @abstractmethod
    def execute(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError


class Invoicer:
    _strategy = None

    def set_strategy(self, strategy: Strategy) -> None:
        if isinstance(strategy, Strategy) is False:
            raise StrategyError("Instance is not Strategy")
        else:
            self._strategy = strategy

    def format(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if self._strategy is None:
            raise ValueError("Use set_strategy to implement method")
        return self._strategy.execute(deepcopy(dataframe))
    

# Different strategies realization


class ExampleFormat(Strategy):
    def execute(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe[dataframe['points'] > 25].copy()
        dataframe['month'] = dataframe['month'].apply(lambda x: 'january')
        return dataframe

class DellFormat1(Strategy):
    def execute(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass # Algorithm realization: reformatting dataframe and return dataframe

    
class DellFormat2(Strategy):
    def execute(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass # Algorithm realization: reformatting dataframe and return dataframe

        
