from copy import copy

import numpy as np
import pandas as pd


class equityAdjustedPrices(pd.Series):

    def __init__(self, price_data):
        price_data.index.name = "index"
        super().__init__(price_data)
    
    @classmethod
    def create_empty(cls):
        equity_prices = cls(pd.Series(dtype="float64"))

        return equity_prices
    
    