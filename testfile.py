from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
data = csvFuturesSimData()
raw_cost = data.get_raw_cost_data("US10")
print(raw_cost)