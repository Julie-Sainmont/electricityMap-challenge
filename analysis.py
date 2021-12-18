# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 19:30:06 2021

@author: julie
"""

import pandas as pd
import numpy as np


def variation_co2_kwh(df):
    if 'datetime' not in df.columns:
        df = df.reset_index()

    df_mean = df.groupby(pd.to_datetime(df['datetime']).dt.hour).mean().reset_index()

    variation_co2_kwh = 100 * (max(df_mean['total_co2_per_MW'])
                               - min(df_mean['total_co2_per_MW'])) / np.mean(df_mean['total_co2_per_MW'])

    print('variation of carbon emission per MWh %.2f %%' % variation_co2_kwh)

    print('the hour where the carbon emission per kWh is the lowest %.f' %
          df_mean[df_mean['total_co2_per_MW'] == min(df_mean['total_co2_per_MW'])].datetime)
