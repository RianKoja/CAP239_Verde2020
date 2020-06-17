########################################################################################################################
# Acquire data from Our World in Data repository (local or remote)
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

import os

# Standard imports:
import pandas as pd


# Use this class to create a list of countries:
class CountryData:
    def __init__(self, country='United States', auto_aquire_data=True):
        self.country = country
        self.df = pd.DataFrame()
        if auto_aquire_data:
            self.df = acquire_data(country=country)


# Use this function to yield the dataframe to be analyzed.
def acquire_data(country='United States', date_ini='2020-02-10', date_end='2020-05-20', acquire_tests=True,
                 start_after_new_cases=50):
    csv_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'mount', 'owid-covid-data.csv')

    if os.path.isfile(csv_filename):  # Read the csv file:
        df = pd.read_csv(csv_filename, index_col=None)
    else:
        print("Downloading COVID-19 data...")
        url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
        df = pd.read_csv(url, index_col=None)
        # Save locally to avoid downloading repeatedly:
        df.to_csv(csv_filename, index=False)

    # Separate country data:
    if country != 'all':
        df = df[df.location == country]
    # Separate date interval:
    df = df[df.date.between(date_ini, date_end, inclusive=True)]
    # Separate useful columns:
    if acquire_tests==True:
        wanted_columns = ['date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_tests', 'new_tests']
    else:
        wanted_columns = ['date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']
        df.dropna(inplace=True)
    if country == 'all':
        wanted_columns.append('location')
    df = df[wanted_columns]    
    # Reset index before next loop:
    df.reset_index(inplace=True)
    # Provide data only after the first day with 50+ new cases
    for ii in range(0, len(df)):
        if df.loc[ii, 'new_cases'] >= start_after_new_cases:
            df = df.drop(range(0, max([0, ii])))
            break
    # df.to_excel('test_df.xlsx') # Use to visualize selected data in excel.
    return df


