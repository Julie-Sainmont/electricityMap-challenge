# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15

PURPOSE:
Create the database from the imported data

@author: julie
"""

import sqlite3
# import pandas as pd

from read_data import read_json, read_generated_energy_data
from parameters import database_file


def create_db():
    """
    Create the database SQLite from the input data

    Returns: Connection to the db

    """
    db_conn = sqlite3.connect(database_file)
    cursor = db_conn.cursor()

    # ---------- Create a table with the energy generated from ENTSO-e data
    print("create generated_energy table")
    # fetch the data
    data = read_generated_energy_data()

    # create the content of the table
    cursor.execute("""DROP TABLE IF EXISTS generated_energy""")
    table_text = """
        CREATE TABLE generated_energy (
        Id INTEGER,
        datetime DATETIME,
        """
    for item in data.columns:
        table_text += item + ' FLOAT(10), \n'
    table_text += "PRIMARY KEY(Id) );"
    # create an empty table
    cursor.execute(table_text)
    # fill the table
    data.to_sql('generated_energy', db_conn, if_exists='append', index=True)

    # ------------ Create the table from the JSON
    emission_factors, type_classification = read_json()
    # -- Table with the emission factors
    print("create emission_factors table")
    # delete the table if already created
    cursor.execute("""DROP TABLE IF EXISTS emission_factors;""")
    # create an empty table
    cursor.execute("""
        CREATE TABLE emission_factors (
        Id INTEGER PRIMARY KEY,
        Type VARCHAR(50),
        Comment VARCHAR(250),
        Source VARCHAR(100),
        Value FLOAT(10)
        );
    """)
    # fill the table
    emission_factors.to_sql('emission_factors', db_conn, if_exists='append', index=False)

    # -- Table with the type_classification
    print("create type_classification table")
    # delete the table if already created
    cursor.execute("""DROP TABLE IF EXISTS type_classification;""")
    # create an empty table
    cursor.execute("""
        CREATE TABLE type_classification (
        Id INTEGER PRIMARY KEY,
        Type VARCHAR(50),
        valueIsLowCarbon FLOAT(10),
        valueIsRenewable FLOAT(10)
        );
    """)
    # fill the table
    type_classification.to_sql('type_classification', db_conn, if_exists='append', index=False)

    # db_conn.close()
    return db_conn
