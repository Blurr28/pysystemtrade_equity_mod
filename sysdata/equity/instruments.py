import pandas as pd
from sysdata.base_data import baseData
from sysobjects.equity_instruments import (
    equityInstrumentWithMetaData,
    listOfEquityInstrumentWithMetaData
)
from syslogging.logger import *

USE_CHILD_CLASS_ERROR = "You need to use a child class of equityInstrumentData"
NOT_IMPLEMENTED_ERROR = "Cost related functions are yet to be implemented"

class equityInstrumentData(baseData):
    def __repr__(self):
        return "equityInstrumentData base class - DO NOT USE"
    
    def __init__(self, log=get_logger("equityInstrumentData")):
        super().__init__(log=log)
    
    def keys(self) -> list:
        return self.get_list_of_instruments()
    
    def __get_item__(self, instrument_code: str):
        return self.get_instrument_data(instrument_code)
    
    def update_slippage_costs(self, instrument_code: str, new_slippage: float):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)
    
    def update_meta_data(self, instrument_code: str, meta_name: str, new_value):
        instrument_object = self.get_instrument_data(instrument_code)
        existing_meta_data = instrument_object.meta_data
        try:
            existing_meta_data_value = getattr(existing_meta_data, meta_name)
        except AttributeError:
            raise Exception(
                "Meta data %s does not exist for instrument %s"
                % (meta_name, instrument_code)
            )
        setattr(existing_meta_data, meta_name, new_value)
        self.add_instrument_data(instrument_object, ignore_duplication=True)
        self.log.debug(
            "Updated %s for %s from %s to %s"
            % (meta_name, instrument_code, existing_meta_data_value, new_value)
        )
    
    def get_all_instrument_data_as_list_of_instrument_objects(
        self,
    ) -> listOfEquityInstrumentWithMetaData:
        all_instrument_codes = self.get_list_of_instruments()
        all_instrument_objects = [
            self.get_instrument_data(instrument_code)
            for instrument_code in all_instrument_codes
        ]
        list_of_instrument_objects = listOfEquityInstrumentWithMetaData(
            all_instrument_objects
        )

        return list_of_instrument_objects
    
    def get_all_instrument_data_as_df(self) -> pd.DataFrame:
        list_of_instrument_objects = (
            self.get_all_instrument_data_as_list_of_instrument_objects()
        )
        list_as_df = list_of_instrument_objects.as_df()

        return list_as_df
    
    def get_instrument_data(
        self, instrument_code: str
    ) -> equityInstrumentWithMetaData:
        if self.is_code_in_data(instrument_code):
            return self._get_instrument_data_without_checking(instrument_code)
        else:
            return equityInstrumentWithMetaData.create_empty()
    
    def delete_instrument_data(self, instrument_code: str, are_you_sure: bool = False):
        self.log.debug("updating log attributes", instrument_code=instrument_code)

        if are_you_sure:
            if self.is_code_in_data(instrument_code):
                self._delete_instrument_data_without_any_warning_be_careful(
                    instrument_code
                )
                self.log.info("Deleted instrument object %s" % instrument_code)

            else:
                # doesn't exist anyway
                self.log.warning("Tried to delete non existent instrument")
        else:
            self.log.error(
                "You need to call delete_instrument_data with a flag to be sure"
            )
    
    def add_instrument_data(
        self,
        instrument_object: equityInstrumentWithMetaData,
        ignore_duplication: bool = False,
    ):
        instrument_code = instrument_object.instrument_code

        self.log.debug("Updating log attributes", instrument_code=instrument_code)

        if self.is_code_in_data(instrument_code):
            if ignore_duplication:
                pass
            else:
                self.log.error(
                    "There is already %s in the data, you have to delete it first"
                    % instrument_code
                )

        self._add_instrument_data_without_checking_for_existing_entry(instrument_object)

        self.log.info("Added instrument object %s" % instrument_object.instrument_code)


    def get_list_of_instruments(self):
        raise NotImplementedError(USE_CHILD_CLASS_ERROR)

    def _get_instrument_data_without_checking(self, instrument_code: str):
        raise NotImplementedError(USE_CHILD_CLASS_ERROR)

    def _delete_instrument_data_without_any_warning_be_careful(
        self, instrument_code: str
    ):
        raise NotImplementedError(USE_CHILD_CLASS_ERROR)

    def _add_instrument_data_without_checking_for_existing_entry(
        self, instrument_object: equityInstrumentWithMetaData
    ):
        raise NotImplementedError(USE_CHILD_CLASS_ERROR)