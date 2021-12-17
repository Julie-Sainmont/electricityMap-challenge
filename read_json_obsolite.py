# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import json

from paramteres import co2_eq_file


# patients_df = pd.read_json(co2_eq_file)
# patients_df.head()


with open(co2_eq_file, 'r') as file:
    # returns JSON object as a dictionary
    co2_eq_dic = json.load(file)

co2_eq_dic.keys()

dict_df = {}
for key1 in co2_eq_dic.keys():
    dict_df[key1] = {}
    for key2 in co2_eq_dic[key1]:
        dict_df[key1][key2] = pd.DataFrame.from_dict(co2_eq_dic[key1][key2], orient='index')
        # dict_df[key1][key2] = pd.json_normalize(co2_eq_dic[key1][key2])


# pd.json_normalize(co2_eq_dic, "emissionFactors", ['defaults',['battery charge', 'battery discharge', 'hydro charge','hydro discharge', 'oil', 'unknown', 'biomass', 'coal', 'gas',
#        'geothermal', 'hydro', 'nuclear', 'solar', 'wind']])

# pd.json_normalize(co2_eq_dic["emissionFactors"], 'defaults',errors="ignore")
# pd.json_normalize(
#     co2_eq_dic,
#     # record_path=["emissionFactors"],
#     meta=["emissionFactors",
#           ["emissionFactors", "defaults"],
#           ],
#     errors="ignore",
# )

# pd.json_normalize(
#     co2_eq_dic,
#     ["emissionFactors", "defaults"],
#     # meta=[
#     #     ["emissionFactors", "defaults"],
#     # ],
#     errors="ignore",
# )


# pd.DataFrame.from_dict(co2_eq_dic['emissionFactors'])


# df = pd.json_normalize(co2_eq_dic['emissionFactors'])
# df.head()

# df = pd.DataFrame.from_dict(pd.json_normalize(co2_eq_dic['emissionFactors']), orient='index')
# df.head()


# # Loop over citizens and their response
# df_answers = pd.DataFrame()
# for kk in range(len(co2_eq_dic)):
#     data = json.loads(co2_eq_dic['emissionFactors'].iloc[kk])
#     df_answers = df_answers.append(
#         pd.json_normalize(
#             data,
#             record_path=["pages", "questions", "answers"],
#             meta=[
#                 "id",
#                 ["pages", "title"],
#                 ["pages", "questions", "title"],
#                 ["pages", "questions", "type"],
#                 ["pages", "questions", "sub_type"],
#             ],
#             record_prefix="answers_",
#             errors="ignore",
#         )
#     )

# dict_data = {}
# for key in co2_eq_dic.keys():
#     dict_data[key] =


# dict_tmp = co2_eq_dic['emissionFactors']
# df_tmp = pd.json_normalize(
#     co2_eq_dic['emissionFactors'],
#     meta=['defautls', 'zoneOverrides'],
#     errors='ignore')
