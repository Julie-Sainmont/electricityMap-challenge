# Electricity map data analysis challenge

Clearning of the generated energy data

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

# Wind onshore and offshore are combined

# Unknown classification for the waste energy production so we will disregard it for this analysis.
Its production is fairly constand throughout the day so it should affect the answer of hourly variation.