import pandas as pd

from syscore.exceptions import missingInstrument
from sysdata.sim.sim_data import simData

from sysobjects.instruments import (
    assetClassesAndInstruments,
    instrumentCosts,
    futuresInstrumentWithMetaData,
)
from sysobjects.equity_adjusted_prices import equityAdjustedPrices

class equitySimData(simData):
    def __repr__(self):
        return "equitySimData object with %d instruments" % len(
            self.get_instrument_list)
    
    def all_asset_classes(self) -> list:
        asset_class_data = self.get_instrument_asset_classes()
        return asset_class_data.all_asset_classes()
    
    def all_instruments_in_asset_class(self, asset_class: str) -> list:
        asset_class_data = self.get_instrument_asset_classes()
        list_of_instrument_codes = self.get_instrument_list()
        asset_class_instrument_list = asset_class_data.all_instruments_in_asset_class(
            asset_class, must_be_in=list_of_instrument_codes
        )
        
        return asset_class_instrument_list
    
    def asset_class_for_instrument(self, instrument_code: str) -> str:
        asset_class_data = self.get_instrument_asset_classes()
        asset_class = asset_class_data[instrument_code]

        return asset_class
    
    def length_of_history_in_days_for_instrument(self, instrument_code: str) -> int:
        return len(self.daily_prices(instrument_code))
    
    def get_raw_price_from_start_date(
        self, instrument_code: str, start_date
    ) -> pd.Series:
        price = self.get_adjusted_equity_price(instrument_code)
        if len(price) == 0:
            raise Exception("Instrument code %s has no data!" % instrument_code)
        
        return price[start_date:]
    
    def get_raw_cost_data(self, instrument_code: str) -> instrumentCosts:
        try:
            cost_data_object = self.get_instrument_object_with_meta_data(
                instrument_code
            )
        except missingInstrument:
            self.log.warning(
                "Cost data missing for %s will use zero costs" % instrument_code
            )
            return instrumentCosts()
        
        spread_cost = self.get_spread_cost(instrument_code)

        instrument_meta_data = cost_data_object.meta_data
        instrument_costs = instrumentCosts.from_meta_data_and_spread_cost(
            instrument_meta_data, spread_cost=spread_cost
        )

        return instrument_costs
    
    def get_value_of_block_price_move(self, instrument_code: str) -> float:
        instr_object = self.get_instrument_object_with_meta_data(instrument_code)
        meta_data = instr_object.meta_data
        block_move_value = meta_data.Pointsize

        return block_move_value
    
    
    def get_instrument_currency(self, instrument_code: str) -> str:
        instr_object = self.get_instrument_object_with_meta_data(instrument_code)
        meta_data = instr_object.meta_data
        currency = meta_data.Currency

        return currency
    
    def get_instrument_asset_classes(self):
        raise NotImplementedError() 
    
    def get_spread_cost(self, instrument_code: str) -> float:
        raise NotImplementedError()
    
    def get_adjusted_equity_price(self, instrument_code: str) -> equityAdjustedPrices:
        raise NotImplementedError()
    
    def get_instrument_meta_data(
            self, instrument_code
    ) -> futuresInstrumentWithMetaData:

        raise NotImplementedError()
    
    def get_instrument_object_with_meta_data(
            self, instrument_code: str
    ) -> futuresInstrumentWithMetaData:

        raise NotImplementedError()