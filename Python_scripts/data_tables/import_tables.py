import pandas as pd
from pathlib import Path

data_source = Path("D:\\mop-dz\\Data\\tables.xlsx")

# read data from excel file
u50 = pd.read_excel(data_source, sheet_name=0)
ew_rate = pd.read_excel(data_source, sheet_name=1)
psr_bound = pd.read_excel(data_source, sheet_name=2)

# unpivot table
ew_rate = pd.melt(ew_rate, ['veh_type', 'road_class', 'lanes', 'max_util_rate'], var_name='max_gradient', value_name='conv_factor')

# save as csv
u50.to_csv('u50.csv')
ew_rate.to_csv('ew_rate.csv')
psr_bound.to_csv('psr_bound.csv')
