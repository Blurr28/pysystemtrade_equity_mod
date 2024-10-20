import pandas as pd
from sysdata.equity.adjusted_prices import equityAdjustedPricesData
from sysobjects.equity_adjusted_prices import equityAdjustedPrices
from syscore.fileutils import (
    resolve_path_and_filename_for_package,
    files_with_extension_in_pathname,
)
from syscore.pandas.pdutils import pd_readcsv
from syscore.constants import arg_not_supplied
from syslogging.logger import *

ADJUSTED_PRICES_DIRECTORY = "data.equity.adjusted_prices_csv"
DATE_INDEX_NAME = "DATETIME"

class csvEquityAdjustedPricesData(equityAdjustedPricesData):

    def __init__(
            self, datapath=arg_not_supplied, log=get_logger("csvEquityPriceData")
    ):
        super().__init__(log=log)

        if datapath is arg_not_supplied:
            datapath = ADJUSTED_PRICES_DIRECTORY
        
        self._datapath = datapath

    def __repr__(self):
        return "csvEquityAdjustedPricesData accessing %s" % self._datapath
    
    @property
    def datapath(self):
        return self._datapath
    
    def get_list_of_instruments(self) -> list:
        return files_with_extension_in_pathname(self.datapath, ".csv")
    
    def _get_adjusted_prices_without_checking(
            self, instrument_code: str
    ) -> equityAdjustedPrices:
        filename = self._filename_given_instrument_code(instrument_code)

        try:
            instrpricedata = pd_readcsv(filename)
        except OSError:
            self.log.warning("Can't find adjusted price file %s" % filename)
            return equityAdjustedPrices.create_empty()
        
        instrpricedata.columns = ["price"]
        instrpricedata = instrpricedata.groupy(level=0).last()
        instrpricedata = pd.Series(instrpricedata.iloc[:, 0])

        instrpricedata = equityAdjustedPrices(instrpricedata)

        return instrpricedata
    
    def _delete_adjusted_prices_without_any_warning_be_careful(
        self, instrument_code
    ):
        raise NotImplementedError(
            "You can't delete adjusted prices stored as a csv - Add to overwrite existing or delete file manually"
        )
    
    def _add_adjusted_prices_without_checking_for_existing_entry(
        self, instrument_code: str, adjusted_price_data: equityAdjustedPrices
    ):
        adjusted_price_data_as_dataframe = pd.DataFrame(adjusted_price_data)
        adjusted_price_data_as_dataframe.columns = ["price"]

        filename = self._filename_given_instrument_code(instrument_code)
        adjusted_price_data_as_dataframe.to_csv(filename, index_label=DATE_INDEX_NAME)

    def _filename_given_instrument_code(self, instrument_code: str):
        return resolve_path_and_filename_for_package(
            self.datapath, "%s.csv" % (instrument_code)
        )