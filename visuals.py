# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15

@author: julie
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

# Full bar plot of % per energy and renewable / non_renewable in MW


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
    fmt = '%.0f%%'  # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(xticks)
    if len(df_mean.columns) == 3:
        df_rel = df_mean[df_mean.columns[1:]]

        for n in df_rel:
            for i, (cs, ab, pc) in enumerate(zip(df_mean.iloc[:, 1:].cumsum(1)[n],
                                                 df_mean[n], df_rel[n])):
                plt.text(i, cs - ab / 2 + i % 2 * 4, str(np.round(pc, 1)) + '%',
                         va='center', ha='center', rotation=20, fontsize=9)
        plt.legend(loc='lower right')
    else:
        plt.legend(loc='upper right')  # 'center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel("Hour of the day")
    # plt.ylabel("percentage")
    if save_graph:
        plt.savefig(output_folder + filename + '.png')
    else:
        plt.show()


def make_visuals(generated_carbon,
                 generated_cao2_per_mw,
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
    # make a simple time serie plot:
    generated_carbon.plot(subplots=True, figsize=(10, 20))
    if save_graph:
        plt.savefig(output_folder + 'energy_production_time_serie.png')
    else:
        plt.show()

    plot_per_hour(generated_cao2_per_mw, "total_co2_per_MW",
                  ylabel_text="carbon per energy ratio (g/MWh)", save_graph=save_graph)
    plot_per_hour(generated_renewable_carbon_ratio, "ratio", yaxis_percentage=True,
                  ylabel_text="carbon from renewable percent", save_graph=save_graph)

    # make it as subplots!
    for col in generated_energy.columns:
        plot_per_hour(generated_energy, col, show_std=False, save_graph=save_graph)

    # Make bar staked per renewable/ non-renewable
    per_col = generated_energy_green_percent.columns[generated_energy_green_percent.columns.str.contains(
        'percent')]
    gen_percent = generated_energy_green_percent[per_col]
    plot_stacked_bar(gen_percent, save_graph=save_graph, filename='generated_energy_green_percent')

    # bar stack per sources:
    plot_stacked_bar(generated_e_percent, save_graph=save_graph, filename='generated_energy_precent_per_sources')
