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
    def __init__(self, country=None, brazil_state='AM', acquire_tests=False, do_dropna=True, date_ini='2020-01-10',
                 date_end='2020-05-20', start_after_new_cases=50):
        if country is None:
            self.country = brazil_state
            self.df = acquire_brazilian_states(state=brazil_state)
        else:
            self.country = country
            self.df = acquire_data(country=country, acquire_tests=acquire_tests, do_dropna=do_dropna, date_ini=date_ini,
                                   date_end=date_end, start_after_new_cases=start_after_new_cases)


# Use this function to yield the dataframe to be analyzed.
def acquire_data(country='United States', date_ini='2020-02-10', date_end='2020-05-20', acquire_tests=False,
                 start_after_new_cases=50, do_dropna=True):
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
    wanted_columns = ['date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    if acquire_tests:
        wanted_columns.extend(['total_tests', 'new_tests'])
    if country == 'all':
        wanted_columns.append('location')
    # Remove unwanted columns:
    df = df[wanted_columns]

    if do_dropna:
        df.dropna(inplace=True)

    # Reset index before next loop:
    df.reset_index(inplace=True)

    # Provide data only after the first day with 50+ new cases
    for ii in range(0, len(df)):
        if df.loc[ii, 'new_cases'] >= start_after_new_cases:
            df = df.drop(range(0, max([0, ii])))
            break
    df['date'] = pd.to_datetime(df['date'])
    # df.to_excel('test_df.xlsx') # Use to visualize selected data in excel.
    return df


def acquire_brazilian_states(state='AM', date_ini='2020-02-10', date_end='2020-05-20',):
    csv_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'mount', 'cases-brazil-states.csv')

    if os.path.isfile(csv_filename):  # Read the csv file:
        df = pd.read_csv(csv_filename, index_col=None)
    else:
        print("Downloading COVID-19 data...")
        url = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv'
        df = pd.read_csv(url, index_col=None)
        # Save locally to avoid downloading repeatedly:
        df.to_csv(csv_filename, index=False)

    # Select desired columns:
    df = df[['date', 'state', 'city', 'newDeaths', 'deaths', 'newCases', 'totalCases']]
    # Use only state columns (no country, no specific city):
    df = df[df['city'] == 'TOTAL']
    df.drop('city', axis=1, inplace=True)
    df = df[df['state'] == state]
    df.drop('state', axis=1, inplace=True)
    # Reorganize to match format from OWID:
    df.columns = ['date', 'new_deaths', 'total_deaths', 'new_cases', 'total_cases']
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.date.between(date_ini, date_end, inclusive=True)]
    return df


if __name__ == "__main__":

    acquire_brazilian_states()
    exit(3)
    objs_list = [CountryData(country=country) for country in ["Brazil"]]
    print("objs_list =", objs_list)
    print("objs_list[0] =", objs_list[0])
    print("objs_list[0].country =", objs_list[0].country)
    print("objs_list[0].df =", objs_list[0].df)

    objs_list = [CountryData(country=country, acquire_tests=True) for country in ["Italy"]]
    print("objs_list =", objs_list)
    print("objs_list[0] =", objs_list[0])
    print("objs_list[0].country =", objs_list[0].country)
    print("objs_list[0].df =", objs_list[0].df)




