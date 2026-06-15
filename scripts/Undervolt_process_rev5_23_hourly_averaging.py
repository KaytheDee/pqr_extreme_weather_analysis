#Import packages 

import numpy as np 
import pandas as pd 
import json 
import glob
import os
import csv
from statsmodels.tsa.seasonal import seasonal_decompose


############## 


### revised function 

def reshape_flags_long(df):
    # Get sensor flag columns
    flag_cols = [c for c in df.columns if c.endswith('_flag')]
    n_sensors = len(flag_cols)

    records = []

    for i in range(1, n_sensors + 1):
        id_col   = f'sensor_{i}_id'
        flag_col = f'sensor_{i}_flag'
        volt_col = f'sensor_{i}_voltage'
        pct_col  = f'sensor_{i}_percent_drop'

        # Skip incomplete sensor groups
        required_cols = ['time', 'site_id', id_col, flag_col, volt_col, pct_col]
        if not all(c in df.columns for c in required_cols):
            continue

        temp = df[required_cols].copy()

        temp = temp.rename(columns={
            id_col:   'sensor_id',
            flag_col: 'flag',
            volt_col: 'voltage',
            pct_col:  'percent_drop'
        })

        records.append(temp)

    if len(records) == 0:
        return pd.DataFrame(
            columns=['time', 'site_id', 'sensor_id', 'flag', 'voltage', 'percent_drop']
        )

    long_df = pd.concat(records, ignore_index=True)

    # Drop rows where sensor_id is missing
    long_df = long_df.dropna(subset=['sensor_id'])

    # Clean data types
    long_df['time'] = pd.to_datetime(long_df['time'], errors='coerce')
    long_df['site_id'] = pd.to_numeric(long_df['site_id'], errors='coerce')
    long_df['flag'] = pd.to_numeric(long_df['flag'], errors='coerce')
    long_df['voltage'] = pd.to_numeric(long_df['voltage'], errors='coerce')
    long_df['percent_drop'] = pd.to_numeric(long_df['percent_drop'], errors='coerce')

    # Drop rows with bad timestamps
    long_df = long_df.dropna(subset=['time'])

    long_df = long_df.sort_values(
        ['site_id', 'sensor_id', 'time']
    ).reset_index(drop=True)

    return long_df
    


### Hourly resampling revised 

def resample_all_sensors_hourly_valid_voltage(
    df,
    min_volt_thresh=23,
    min_valid_fraction=0.5,
    expected_per_hour=30
):
    df = df.copy()
    df['time'] = pd.to_datetime(df['time'])
    df['voltage'] = pd.to_numeric(df['voltage'], errors='coerce')

    df['valid_voltage'] = df['voltage'].where(df['voltage'] > min_volt_thresh)
    df['is_valid_voltage'] = (df['voltage'] > min_volt_thresh).astype(int)

    df = df.set_index('time')

    hourly = (
        df.groupby(['site_id', 'sensor_id'])
          .resample('1h')
          .agg({
              'valid_voltage': 'mean',
              'is_valid_voltage': 'sum',
              'voltage': 'count'
          })
    )

    hourly.columns = [
        'voltage',
        'n_valid_timestamps',
        'n_available_timestamps'
    ]

    hourly = hourly.reset_index()

    hourly['expected_timestamps'] = expected_per_hour

    hourly['valid_fraction'] = (
        hourly['n_valid_timestamps'] / hourly['expected_timestamps']
    )

    hourly.loc[
        hourly['valid_fraction'] < min_valid_fraction,
        'voltage'
    ] = np.nan

    hourly['voltage'] = hourly['voltage'].round(2)
    hourly['valid_fraction'] = hourly['valid_fraction'].round(3)

    hourly = hourly[
        ['time', 'site_id', 'sensor_id',
         'voltage', 'valid_fraction',
         'n_available_timestamps',
         'n_valid_timestamps',
         'expected_timestamps']
    ]

    return hourly



############## 



## Undervoltage low limit threshold 
min_volt_thresh = 23 


### Read cleaned_flags  
cleaned_flags_bounds = pd.read_csv(
    '/work/pi_jtaneja_umass_edu/kdonkor_umass_edu/Geospatial_Files/Undervoltage_Analysis/undervolt_cleaned_flags_all_23_rev5.csv',
    low_memory=False
)

## convert to long format 
cleaned_flags_bounds = reshape_flags_long(cleaned_flags_bounds)


## hourly resampling 
hourly_voltages_df = resample_all_sensors_hourly_valid_voltage(
    cleaned_flags_bounds,
    min_volt_thresh = min_volt_thresh,
    min_valid_fraction=0.5,
    expected_per_hour=30
)


## Save to file 
hourly_voltages_df.to_csv('/work/pi_jtaneja_umass_edu/kdonkor_umass_edu/Geospatial_Files/Undervoltage_Analysis/undervolt_hourly_voltages_df_23.csv', index=False)





