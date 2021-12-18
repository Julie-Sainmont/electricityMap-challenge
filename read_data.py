# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15

PURPOSE:
--------
Read the input data, make the basic cleaning and pretreatment of the data
Export DataFrame ready for use

@author: julie
"""

import pandas as pd
import numpy as np
import json
from parameters import generated_energy_file, co2_eq_file, window_outlier_detection


def outlier_detection(df, window=20):
    for col_name in df.columns:
        df['median'] = df[col_name].rolling(window).median()  # .fillna(method='bfill').fillna(method='ffill')
        df['std'] = df[col_name].rolling(window).std()  # .fillna(method='bfill').fillna(method='ffill')
        # filter setup
        df[col_name] = np.where(np.logical_or(
            pd.isnull(df['median']),
            np.logical_and(
                df[col_name] <= df['median'] + 3 * df['std'],
                df[col_name] >= df['median'] - 3 * df['std'])
        ),
            df[col_name],
            np.nan
        )
    df.drop(['median', 'std'], axis=1, inplace=True)
    return df


def read_generated_energy_data():
    """
    read the input file containing the generated energy consumption
    perfrom general cleaning of the data set:
        - treatment of the columns
        - removal of the obvious outliers
    Returns:
        generated_energy (DataFrame): The df containing the generated energy.

    """
    # read the file and adjust to separate in columns
    generated_energy = pd.read_csv(generated_energy_file, sep=",")
    col_names = generated_energy.columns.str.split(',').tolist()
    generated_energy = generated_energy.iloc[:, 0].str.split(',', expand=True)
    generated_energy.columns = [item.replace('"', '') for item in col_names[0]]

    # get the datetime from the MTU columnThe c
    generated_energy['datetime'] = pd.to_datetime(generated_energy['MTU'].str.replace('"', '').str[0:17])

    generated_energy = generated_energy.drop(['MTU', 'Area'], axis=1).set_index('datetime')

    # convert the value to numeric
    for col in generated_energy.columns:
        generated_energy[col] = generated_energy[col].str.replace('"', '')
        generated_energy[col] = pd.to_numeric(generated_energy[col], errors='coerce')

    # drop the columns with only nan
    generated_energy = generated_energy.dropna(axis=1, how='all')

    # simplify header
    generated_energy.columns = [item.replace(' ', '') + 'MW' for item in list(
        zip(*generated_energy.columns.str.split("  - ")))[0]]

    # remove outlier
    # clearly visible on this time serie visualisation: generated_energy.plot(subplots=True, figsize=(10, 20))
    generated_energy_cleaned = outlier_detection(generated_energy, window=window_outlier_detection)
    # check that they are removed: generated_energy_cleaned.plot(subplots=True, figsize=(10, 20))

    return generated_energy_cleaned.fillna(0)


def read_json():
    """
    Read the json file with info of the emissions per type of energy source,
    and classification of the type of energy source

    Returns:
        emission_factors (DataFrame): how much each source of energy is producing carbon,
                 with the source and potential comments
        type_classification (DataFrame): per type of electricity source, classification if low in carbon & is renewable.

    """
    with open(co2_eq_file, 'r') as file:
        # returns JSON object as a dictionary
        co2_eq_dic = json.load(file)

    # make a dictionary of df 2 level down
    dict_df = {}
    for key1 in co2_eq_dic.keys():
        dict_df[key1] = {}
        for key2 in co2_eq_dic[key1]:
            dict_df[key1][key2] = pd.DataFrame.from_dict(co2_eq_dic[key1][key2], orient='index')

    # make a dictionary of tables with info at 1 level, i.e. on 'emissionFactors', 'isLowCarbon', 'isRenewable'
    info_dict = {}
    for info in ['emissionFactors', 'isLowCarbon', 'isRenewable']:
        info_dict[info] = dict_df[info]['defaults'].rename(columns={0: 'value'})
        # correct for dk2
        if 'DK-DK2' in dict_df[info]['zoneOverrides'].index:
            for e_type in dict_df[info]['zoneOverrides'].loc['DK-DK2'].index:
                if type(dict_df[info]['zoneOverrides'].loc['DK-DK2'].loc[e_type]) is dict:
                    correction = dict_df[info]['zoneOverrides'].loc['DK-DK2'].loc[e_type]['value']
                    if ~pd.isnull(correction):
                        info_dict[info].loc[e_type, 'value'] = correction

    # treat the emission factor table
    emission_factors = info_dict['emissionFactors'].reset_index()\
        .rename(columns={"index": 'Type', "_comment": "comment"})
    emission_factors.columns = emission_factors.columns.str.capitalize()

    # combine the category of the different type of electricity source
    type_classification = pd.merge(info_dict['isLowCarbon'], info_dict['isRenewable'],
                                   how='outer',
                                   left_index=True, right_index=True,
                                   suffixes=("IsLowCarbon", 'IsRenewable'))
    type_classification = type_classification.reset_index().rename(columns={'index': 'Type'})

    return emission_factors, type_classification
