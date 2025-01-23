import pandas as pd
from systems.rawdata import RawData
from systems.system_cache import input, diagnostic, output

NA = "Method not applicable for equity class."
TBD = "To be developed."

class EquityRawData(RawData):

    def rolls_per_year(self, instrument_code):
        raise NotImplementedError(NA)
    
    def get_instrument_raw_carry_data(self, instrument_code):
        raise NotImplementedError(NA)
    
    def raw_futures_roll(self, instrument_code):
        raise NotImplementedError(NA)
    
    def roll_differentials(self, instrument_code):
        raise NotImplementedError(NA)
    
    def annualised_roll(self, instrument_code):
        raise NotImplementedError(NA)
    
    def daily_annualised_roll(self, instrument_code):
        raise NotImplementedError(NA)
    
    def raw_carry(self, instrument_code):
        raise NotImplementedError(NA)
    
    def smoothed_carry(self, instrument_code, smooth_days = 90):
        raise NotImplementedError(NA)
    
    def _by_asset_class_median_carry_for_asset_class(self, asset_class, smooth_days = 90):
        raise NotImplementedError(NA)
    
    def median_carry_for_asset_class(self, instrument_code):
        raise NotImplementedError(NA)

    @diagnostic
    def _by_asset_class_daily_vol_normalised_price_for_asset_class(self, asset_class):
        raise NotImplementedError(TBD)

    @diagnostic
    def daily_vol_normalised_price_for_asset_class_with_redundant_instrument_code(self, instrument_code, asset_class):
        raise NotImplementedError(TBD)
    
    @output
    def normalised_price_for_asset_class(self, instrument_code):
        raise NotImplementedError(TBD)
    
    def daily_denominator_price(self, instrument_code: str) -> pd.Series:
        return self.get_daily_prices(instrument_code)

