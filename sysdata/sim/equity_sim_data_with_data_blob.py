from sysdata.sim.equity_sim_data import equitySimData

from sysdata.equity.adjusted_prices import equityAdjustedPricesData
from sysdata.fx.spotfx import fxPricesData
from sysdata.equity.instruments import equityInstrumentData
from sysdata.data_blob import dataBlob

from sysobjects.instruments import (
    assetClassesAndInstruments,
    futuresInstrumentWithMetaData,
)
from syscore.exceptions import missingData
from sysobjects.spot_fx_prices import fxPrices
from sysobjects.equity_adjusted_prices import equityAdjustedPrices


class genericBlobUsingEquitySimData(equitySimData):

    def __init__(self, data: dataBlob):
        super().__init__(log=data.log)
        self._data = data
    
    def get_instrument_list(self):
        return self.db_equity_adjusted_prices_data.get_list_of_instruments()
    
    def _get_fx_data_from_start_date(
        self, currency1:str, currency2: str, start_date
    ) -> fxPrices:
        fx_code = currency1 + currency2
        data = self.db_fx_prices_data.get_fx_prices(fx_code)

        data_after_start = data[start_date:]

        return data_after_start
    
    def get_instrument_asset_classes(self) -> assetClassesAndInstruments:
        all_instrument_data = self.get_all_instrument_data_as_df()
        asset_classes = all_instrument_data["AssetClass"]
        asset_class_data = assetClassesAndInstruments.from_pd_series(asset_classes)

        return asset_class_data
    
    def get_all_instrument_data_as_df(self):
        """Not yet functioning"""
        all_instrument_data = (
            self.db_equity_instrument_data.get_all_instrument_data_as_df()
        )
        instrument_list = self.get_instrument_list()
        all_instrument_data = all_instrument_data[
            all_instrument_data.index.isin(instrument_list)
        ]

        return all_instrument_data
    
    def get_adjusted_equity_price(
        self, instrument_code: str
    ) -> equityAdjustedPrices:
        data = self.db_equity_adjusted_prices_data.get_adjusted_prices(instrument_code)

        return data
    
    def get_instrument_meta_data(
        self, instrument_code: str
    ) -> futuresInstrumentWithMetaData:
        """Not implemented/ functioning"""
        return self.get_instrument_object_wit_meta_data(instrument_code)
    
    def get_instrument_object_with_meta_data(
        self, instrument_code: str
    ) -> futuresInstrumentWithMetaData:
        """Not functioning"""
        instrument = self.db_equity_instrument_data.get_instrument_data(
            instrument_code
        )

        return instrument
    
    def get_spread_cost(self, instrument_code: str) -> float:
        """Not working/ needs to be implemented"""
        return self.db_spread_cost_data.get_spread_cost(instrument_code)
    
    @property
    def data(self):
        return self._data
    
    @property
    def db_fx_prices_data(self) -> fxPricesData:
        """Not functioning"""
        return self.data.db_fx_prices
        
    @property
    def db_equity_adjusted_prices_data(self) -> equityAdjustedPricesData:
        return self.data.db_equity_adjusted_prices
    
    @property
    def db_equity_instrument_data(self) -> equityInstrumentData:
        return self.data.db_equity_instrument
    
    @property
    def db_spread_cost_data(self):
        """Not implemented"""
        return self.data.db_spread_cost