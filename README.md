# Electricity map data analysis challenge

## Folder structure
The python code is present in the main folder.
inputs: contains the data extract used for the analysis. They come from outside sources (ENTSO-e and electricityMap git repo)
data: contains the database file created with the data imported
outputs: the outputs files from the code, it contains mainly the plots/visuls
report: the LaTeX code to produce the report

## Python code
The data extract, database creating, fetch, data prepaparation and visualisation are run by running the main.py code.
Export of the plots is controled by the parameters save_graph paramter in the paramter.py file.

## Clearning of the generated energy data

# Read the csv
The columns wasnt getting separated into columns automatically so some preprocessing was done:
 - the column names get extracted separately to transformed into list of header
 - the data is then split into columns
 - the header are reallocated to the data

# treatment on the columns
The datetime is extracted from the MTU columns and allocated to the beginning of the hour of each measurement
All the numeric columns are converted to numeric (string before)
Time serie visualisation show a pic of consumption for the gas and the hard coal:
 the outliers are removed with a rolling windows - disregarding everything that is outside of 3 times the standard deviation

The Wind onshore and offshore columns are combined into one wind column.

The Wast source has an unknown classification for the waste energy production so we will disregard it for this analysis.
Its production is fairly constant throughout the day so it should not affect the hourly variation analysis.


## Report
The report is done in LateX. the .tex file can the compiled with pdflatex to produce the pdf.
To ensure that all the reference gets updated report should be compiled twice.


