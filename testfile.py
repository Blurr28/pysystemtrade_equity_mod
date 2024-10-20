from sysdata.csv.csv_equity_adjusted_prices import csvEquityAdjustedPricesData

data = csvEquityAdjustedPricesData()
print(data.get_list_of_instruments())