from syscore.constants import arg_not_supplied
from sysdata.csv.csv_equity_adjusted_prices import csvEquityAdjustedPricesData
from sysdata.csv.csv_spot_fx import csvFxPricesData
from sysdata.csv.csv_equity_instrument_data import csvEquityInstrumentData
#from sysdata.csv.csv_spread_cost import csvSpreadCostData

from sysdata.data_blob import dataBlob
from sysdata.sim.equity_sim_data_with_data_blob import genericBlobUsingEquitySimData

from syslogging.logger import *

class csvEquitySimData(genericBlobUsingEquitySimData):

    def __init__(
        self, csv_data_paths=arg_not_supplied, log=get_logger("csvEquitySimData")
    ):
        data = dataBlob(
            log=log,
            csv_data_paths=csv_data_paths,
            class_list=[
                csvEquityAdjustedPricesData,
                csvEquityInstrumentData,
                csvFxPricesData,
                #csvSpreadCostData
            ],
         )
        
        super().__init__(data=data)
    
    def __repr__(self):
        return "csvEquitySimData object with %d instruments" % len(
            self.get_instrument_list()
        )
