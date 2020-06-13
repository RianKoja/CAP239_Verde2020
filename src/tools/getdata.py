########################################################################################################################
# Acquire data from Our World in Data repository (local or remote)
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard imports:
import pandas as pd
import os


# Use this function to yield the dataframe to be analyzed.
def acquire_data(country='United States', date_ini='2020-02-10', date_end='2020-05-20'):
    xls_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data', 'covid-19-data',
                                'owid-covid-data.xlsx')

    if os.path.isfile(xls_filename):  # Read the csv file:
        print("Using local data for COVID-19 cases...")
        df = pd.read_excel(xls_filename)
    else:
        print("Using data online for COVID-19 cases...")
        url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
        df = pd.read_csv(url, index_col=0)

    # Separate country data:
    if country != 'all':
        df = df[df.location == country]
    # Separate date interval:
    df = df[df.date.between(date_ini, date_end, inclusive=True)].reset_index()
    # Separate useful columns:
    wanted_columns = ['date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    if country == 'all':
        wanted_columns.append('location')
    df = df[wanted_columns]
    # TODO: Separate only after the first day with 50+ cases
    # df.to_excel('test_df.xlsx') # Use to visualize selected data in excel.
    return df
