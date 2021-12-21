# Electricity map data analysis challenge

## Folder structure
The python code is present in the main folder.\

Subfolders:
 - inputs: contains the data extract used for the analysis. They come from outside sources (ENTSO-e and electricityMap git repo)\
 - data: contains the database file created with the data imported\
 - outputs: contains the outputs files from the code, it contains mainly the plots/visuls\
 - report: contains the LaTeX code to produce the report

## Python code
The data extract, database creation, fetching, data prepaparation and visualisation are run by compiling the main.py code.\
The plots export is controled by the parameters save_graph parameter in the parameters.py file.

### Clearning of the generated energy data

#### Read the csv
The columns were not being separated into columns automatically so some preprocessing was done:
 - the column names get extracted separately to be transformed into list of headers,
 - the data is then split into columns,
 - the headers are reallocated to the data.

#### Treatment on the columns
The datetime is extracted from the MTU columns and allocated to the beginning of the hour of each measurement.\

All the numeric columns are converted to numeric (string beforehand).\

The time series visualisation shows a peak of consumption for the gas and the hard coal:
 - the outliers are removed with rolling windows - disregarding everything that is outside of 3 times the standard deviation

The Wind onshore and offshore columns are combined into one 'Wind' column.

The Waste source has an unknown classification for the waste energy production so it is disregarded for the analysis.
Its production is fairly constant throughout the day so it should not strongly affect the hourly variation analysis.

The columns that contain only zeros are removed.

## Report
The report is done in LateX. The .tex file can the compiled with pdflatex to produce the pdf.
To ensure that all the references get updated, the report should be compiled twice.

The figures are fetched directly in the 'outputs' folder so updates on the visuals from the python code will be automatically
reflected in the report (after it is recompiled).
