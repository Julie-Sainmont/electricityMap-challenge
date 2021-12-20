# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 18:23:21 2021

PURPOSE:
-------
Make some simple visualisation to understand when it is the best time to use electricity

@author: julie
"""

from create_sqlite import create_db
from data_preparation import data_combination
from visuals import make_visuals
from analysis import variation_co2_kwh

# Read the data and create the database
db_conn = create_db()

# data combination
(generated_carbon,
 generated_co2_per_mw,
 generated_renewable_carbon_ratio,
 generated_energy,
 generated_energy_green_percent,
 generated_e_percent) = data_combination(db_conn)

# Close the database file
db_conn.close()

# make some plots
make_visuals(generated_carbon,
             generated_co2_per_mw,
             generated_renewable_carbon_ratio,
             generated_energy,
             generated_energy_green_percent,
             generated_e_percent
             )

# gets some numbers
variation_co2_kwh(generated_co2_per_mw)
