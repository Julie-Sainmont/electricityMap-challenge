# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15

@author: julie
"""

generated_energy_file = "inputs/Actual Generation per Production Type_202001010000-202101010000.csv"
co2_eq_file = 'inputs/co2eq_parameters.json'

database_file = "data/energy.db"

window_outlier_detection = 10

dict_corr = {
    'BiomassMW': "biomass",
    'FossilGasMW': "gas",
    'FossilHardcoalMW': "coal",
    'FossilOilMW': "oil",
    'SolarMW': "solar",
    'WindMW': "wind"
}

output_folder = 'outputs/'
save_graph = True
