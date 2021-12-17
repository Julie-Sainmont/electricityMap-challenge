# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15

PURPOSE:
Prepare the tables so that they are ready to be visualised

@author: julie
"""
import pandas as pd
import numpy as np

from parameters import dict_corr


def print_head_table(db_conn):
    print('generated_energy', pd.read_sql("SELECT * FROM generated_energy LIMIT 5", db_conn))
    print("emission_factors", pd.read_sql("SELECT * FROM emission_factors LIMIT 5", db_conn))
    print("type_classification", pd.read_sql("SELECT * FROM type_classification LIMIT 5", db_conn))


def df_transform_per_category(df_e, co2_em, dict_corr, in_co2=False, for_renewable=np.nan):
    df_return = pd.DataFrame()
    # Make sure that datetime is in index, and keep only the relevant columns
    if 'datetime' in df_e.columns:
        df_e = df_e.set_index('datetime')
    df_e = df_e[dict_corr.keys()]

    for col in dict_corr.keys():
        if in_co2:
            conv_co2 = co2_em.loc[dict_corr[col]]['carbonEmission']
            text_co2 = '_co2'
        else:
            conv_co2 = 1
            text_co2 = ''
        if pd.isnull(for_renewable):
            green = 1
            text_renewable = ''
        elif for_renewable:
            green = co2_em.loc[dict_corr[col]]['valueIsRenewable']
            text_renewable = '_from_renewable'
        else:
            green = co2_em.loc[dict_corr[col]]['valueIsNonRenewable']
            text_renewable = '_from_non_renewable'
        df_return[dict_corr[col]] = df_e[col] * conv_co2 * green
    df_return['total' + text_co2 + text_renewable] = df_return.sum(axis=1)
    return df_return


def data_combination(db_conn):
    """
    Fetch the info from the database, make some data combination,
    so that the data is ready to be visualised

    Args:
        db_conn: Data base connection.

    Returns:
        generated_carbon (df): Time serie of the carbon produced per sources.
        generated_co2_per_mw (df): Time serie of the carbon per energy produced per sources.
        generated_renewable_carbon_ratio (df): Time serie of the ratio of the carbon
                  produced from energy sources versus non energy sources
        generated_energy (df): Time serie of the energy per sources.
        generated_energy_green_percent (df): Time serie of the energy percentage from renewable/non-renewable
        generated_e_percent (df): Time serie of the energy percentage per sources

    """
    # visualise the header of the tables from the database (db)
    # print_head_table(db_conn)

    # create a table that combine the information on the source type of energy
    sql_script = """
    SELECT ef.Type,
           ef.Value AS carbonEmission,
           tc.valueIsLowCarbon,
           tc.valueIsRenewable,
           CASE WHEN tc.valueIsRenewable = TRUE THEN FALSE ELSE TRUE END AS valueIsNonRenewable
    FROM emission_factors ef
      LEFT JOIN type_classification tc
      ON ef.Type = tc.Type
    """
    carbon_emmission = pd.read_sql(sql_script, db_conn).set_index('Type')

    # Generated energy in MW per type + total
    generated_energy = pd.read_sql("SELECT * FROM generated_energy", db_conn).set_index('datetime')
    generated_energy["WindWM"] = generated_energy['WindOffshoreWM'] + generated_energy['WindOnshoreWM']
    generated_energy.drop(['Id', "WindOffshoreWM", "WindOnshoreWM"], axis=1, inplace=True)
    type_energy_list = generated_energy.columns
    generated_energy['total_MW'] = generated_energy.sum(axis=1)

    generated_e_percent = pd.DataFrame()
    for col in type_energy_list:
        generated_e_percent[col] = 100 * generated_energy[col] / generated_energy['total_MW']

    generated_energy_from_renewable = df_transform_per_category(
        generated_energy, carbon_emmission, dict_corr, in_co2=False, for_renewable=True)
    generated_energy_from_non_renewable = df_transform_per_category(
        generated_energy, carbon_emmission, dict_corr, in_co2=False, for_renewable=False)

    generated_energy_green_percent = pd.concat([generated_energy_from_renewable[['total_from_renewable']],
                                                generated_energy_from_non_renewable[['total_from_non_renewable']]
                                                ], axis=1
                                               )
    generated_energy_green_percent['total'] = generated_energy_green_percent.sum(axis=1)
    for col in ['from_renewable', 'from_non_renewable']:
        generated_energy_green_percent['percent_' + col] = 100 * \
            generated_energy_green_percent['total_' + col] / generated_energy_green_percent['total']

    # Generated carbon per type + total
    generated_carbon = df_transform_per_category(
        generated_energy, carbon_emmission, dict_corr, in_co2=True, for_renewable=np.nan)

    # Generated carbon of renewable sources + total
    generated_renewable_carbon = df_transform_per_category(
        generated_energy, carbon_emmission, dict_corr, in_co2=True, for_renewable=True)

    # Generated carbon from renewable versus total ratio
    generated_renewable_carbon_ratio = pd.merge(generated_carbon['total_co2'],
                                                generated_renewable_carbon['total_co2_from_renewable'],
                                                how='outer',
                                                left_index=True, right_index=True)
    generated_renewable_carbon_ratio['ratio'] = 100 *\
        generated_renewable_carbon_ratio['total_co2_from_renewable'] / \
        generated_renewable_carbon_ratio['total_co2']

    # Generated carbon / MW
    generated_carbon_mw = pd.merge(generated_energy,
                                   generated_carbon,
                                   how='outer',
                                   left_index=True, right_index=True)
    generated_co2_per_mw = pd.DataFrame()
    dict_corr2 = dict_corr.copy()
    dict_corr2["total_MW"] = 'total_co2'
    for col in dict_corr2.keys():
        generated_co2_per_mw[dict_corr2[col]] = generated_carbon_mw[dict_corr2[col]] / generated_carbon_mw[col]
    generated_co2_per_mw.rename(columns={'total_co2': 'total_co2_per_MW'}, inplace=True)
    # generated_co2_per_mw['total_co2'] = generated_co2_per_mw.sum(axis=1)

    return (generated_carbon,
            generated_co2_per_mw,
            generated_renewable_carbon_ratio,
            generated_energy,
            generated_energy_green_percent,
            generated_e_percent)
