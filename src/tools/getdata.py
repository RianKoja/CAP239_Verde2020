########################################################################################################################
# Acquire data from Our World in Data repository (local or remote)
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

import os

# Standard imports:
import pandas as pd


# Use this class to create a list of countries:
class CovidData:
    def __init__(self, country=None, brazil_state=None, acquire_tests=False, do_dropna=True, date_ini='2020-01-10',
                 date_end='2020-05-20', start_after_new_cases=50):
        if brazil_state is not None:
            self.location = brazil_state
            self.df = acquire_brazilian_states(state=brazil_state)
        elif country is not None:
            self.location = country
            self.df = acquire_data(country=country, acquire_tests=acquire_tests, do_dropna=do_dropna, date_ini=date_ini,
                                   date_end=date_end, start_after_new_cases=start_after_new_cases)
        else:
            self.location = 'Rocinha'
            self.df = acquire_rocinha()


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


def acquire_brazilian_states(state='AM', date_ini='2020-02-10', date_end='2020-05-20'):
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


def acquire_rocinha(date_ini='2020-02-10', date_end='2020-05-20'):
    from operator import itemgetter
    csv_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'mount', 'rocinha.csv')

    if not os.path.isfile(csv_filename):  # Read the csv file:
        print("File not found for Rocinha data, check this, it should have been submitted in the repository.")
        exit(4)
    df = pd.read_csv(csv_filename)
    df = df[['datas', 'confirmados', 'confirmados_acum', 'obitos_acum']]
    df['date'] = df['datas'].apply(lambda x: "2020-" + '-'.join(itemgetter(1, 0)(x.split('/'))))

    df['total_cases'] = df['confirmados_acum']
    df['new_cases'] = df['confirmados']
    df['total_deaths'] = df['obitos_acum']
    total_deaths = df['total_deaths'].to_list()
    daily_death = [0] + [x - total_deaths[i - 1] for i, x in enumerate(total_deaths)][1:]
    df['new_deaths'] = daily_death
    df.drop(['datas', 'confirmados', 'confirmados_acum', 'obitos_acum'], axis=1, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    # Separate date interval:
    df = df[df.date.between(date_ini, date_end, inclusive=True)]
    return df


if __name__ == "__main__":

    acquire_rocinha()

    acquire_brazilian_states()

    objs_list = [CovidData(country=country) for country in ["Brazil"]]

    objs_list2 = [CovidData(country=country, acquire_tests=True) for country in ["Italy"]]





