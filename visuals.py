# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15

@author: julie
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.dates import DateFormatter
import seaborn as sns
import pandas as pd
import numpy as np
from parameters import save_graph, output_folder


def plot_per_hour(df, col_name, yaxis_percentage=False, ylabel_text=None, show_std=True, save_graph=False):
    """
    Plot (bar) the data from the dataframe and from the specific
    columns against the datetime column.

    Args:
        df (DataFrame): The data to be plotted
              it must contain the datetime column either as a columns as in index
        col_name (str): The name of the column to plot.
        yaxis_percentage (Boolean, optional): should the y axis be in percentages
            Defaults to False.
        ylabel_text (TYPE, optional): The text to be added on the yaxis.
            if None, write the colname
            Defaults to None.

    Returns:
        None.

    """
    if 'datetime' not in df.columns:
        df = df.reset_index()
    if 'datetime' not in df.columns or col_name not in df.columns:
        print(f'the data is missing either the datetime or the {col_name} column')
        return
    dfmean = df.groupby(pd.to_datetime(df['datetime']).dt.hour)[col_name].agg([np.mean, np.std])
    if show_std:
        ax = dfmean.plot(kind='bar', y='mean', yerr='std', legend=False, figsize=(7, 4))
    else:
        ax = dfmean.plot(kind='bar', y='mean', legend=False, figsize=(7, 4))
    if yaxis_percentage:
        fmt = '%.0f%%'  # Format you want the ticks, e.g. '40%'
        xticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(xticks)
    if pd.isnull(ylabel_text):
        ylabel_text = col_name
    plt.xlabel("Hour of the day")
    plt.ylabel(ylabel_text)
    if save_graph:
        plt.savefig(output_folder + ylabel_text.replace(' ', '_').split('_(')[0] + '.png')
    else:
        plt.show()
    return


def plot_stacked_bar(df, save_graph=False, filename='graph'):
    if 'datetime' not in df.columns:
        df = df.reset_index()
    if 'datetime' not in df.columns:
        print('the data is missing either the datetime')
        return
    # plot a Stacked Bar Chart using matplotlib
    df_mean = df.groupby(pd.to_datetime(df['datetime']).dt.hour).mean().reset_index()
    if len(df_mean.columns) == 3:
        color_palette = ['forestgreen', 'darkorange']
    else:
        color_palette = sns.color_palette()
    ax = df_mean.plot(
        x='datetime',
        kind='bar',
        stacked=True,
        mark_right=True,
        figsize=(10, 7),
        color=color_palette)
    # format the ylabel to have it in %
    xticks = mtick.FormatStrFormatter('%.0f%%')
    ax.yaxis.set_major_formatter(xticks)
    if len(df_mean.columns) == 3:
        df_rel = df_mean[df_mean.columns[1:]]

        for n in df_rel:
            for i, (cs, ab, pc) in enumerate(zip(df_mean.iloc[:, 1:].cumsum(1)[n],
                                                 df_mean[n], df_rel[n])):
                plt.text(i, cs - ab / 2 + i % 2 * 4, str(np.round(pc, 1)) + '%',
                         va='center', ha='center', rotation=20, fontsize=9)

    plt.legend(loc='lower right')
    plt.xlabel("Hour of the day")
    if save_graph:
        plt.savefig(output_folder + filename + '.png')
    else:
        plt.show()
    return


def plot_time_series(df, save_graph=False):
    """
    Plot time serie

    Args:
        df (dataframe): the dataframe to plot.
        save_graph (boolean, optional): rather the plot should be saved or only displayed.
              Defaults to False.

    Returns:
        None.

    """
    df.index = pd.to_datetime(df.index)
    # make a simple time serie plot:
    ax = df.plot(subplots=True, figsize=(10, 18))
    ax[-1].xaxis.set_major_formatter(DateFormatter("%d-%m-%Y"))
    # Reserve space for axis labels
    ax[-1].set_xlabel('')
    ax[-1].set_ylabel('Carbon produced (mass)')
    ax[3].set_ylabel('Energy emitted (MWh)')
    if save_graph:
        plt.savefig(output_folder + 'energy_production_time_serie.png')
    else:
        plt.show()
    return


def make_visuals(generated_carbon,
                 generated_co2_per_mw,
                 generated_renewable_carbon_ratio,
                 generated_energy,
                 generated_energy_green_percent,
                 generated_e_percent
                 ):
    """
    Make some visuals with the main df

    Args:
        generated_carbon (df): Time serie of the carbon produced per sources.
        generated_co2_per_mw (df): Time serie of the carbon per energy produced per sources.
        generated_renewable_carbon_ratio (df): Time serie of the ratio of the carbon
                  produced from energy sources versus non energy sources
        generated_energy (df): Time serie of the energy per sources.
        generated_energy_green_percent (df): Time serie of the energy percentage from renewable/non-renewable
        generated_e_percent (df): Time serie of the energy percentage per sources

    Returns:
        None.

    """
    df_time_serie = pd.concat([generated_energy.drop('totalMW', axis=1), generated_carbon[['total_co2']]], axis=1)
    df_time_serie.columns = df_time_serie.columns.str.replace('MW', '')
    plot_time_series(df_time_serie, save_graph=save_graph)

    plot_per_hour(generated_co2_per_mw, "total_co2_per_MW",
                  ylabel_text="carbon per energy ratio (mass/MWh)", save_graph=save_graph)
    plot_per_hour(generated_renewable_carbon_ratio, "ratio", yaxis_percentage=True,
                  ylabel_text="carbon from renewable percent", save_graph=save_graph)

    # make it as subplots!
    generated_energy.columns = generated_energy.columns.str.replace("MW", " (MWh)")
    for col in generated_energy.columns:
        plot_per_hour(generated_energy, col, show_std=False, save_graph=save_graph)

    # Make bar staked per renewable/ non-renewable
    per_col = generated_energy_green_percent.columns[generated_energy_green_percent.columns.str.contains(
        'percent')]
    gen_percent = generated_energy_green_percent[per_col]
    plot_stacked_bar(gen_percent, save_graph=save_graph, filename='generated_energy_green_percent')

    # Stacked bar per sources:
    # re-order the columns to start witht the renewables:
    generated_e_percent = generated_e_percent[
        ['WindMW', 'BiomassMW', 'SolarMW', 'FossilGasMW', 'FossilHardcoalMW', 'FossilOilMW']]
    plot_stacked_bar(generated_e_percent, save_graph=save_graph, filename='generated_energy_precent_per_sources')
