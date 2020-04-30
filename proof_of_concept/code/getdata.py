########################################################################################################################
# Acquire a table of financial indicators for Brazilian real state funds from a .xlsx file in the resources directory.
# Treats the data before usage.
#
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard imports:
import pandas as pd
import os

def make_numeric(df, name):
    for ii in range(len(df)):
        print(df[name][ii])
        if not pd.isnull(df[name][ii]):
            df[name][ii] = eval(str(df[name][ii]).replace(" ", "").replace(".", "").replace(",", ".").replace("R$", "").replace("%", "/100"))
    df[[name]] = df[[name]].astype('float64')
    return df


# Use this function to yield the dataframe tobe analyzed. Suggested to create new functions if the source of data is to
# be changed
def acquire_data(xlsx_name):
    xls_filename = os.path.join(os.getcwd(), 'resources', xlsx_name)
    #  Read the csv file:
    df = pd.read_excel(xls_filename)
    # Remove duplicate entries, if any:
    df = df.drop_duplicates()
    # fix numeric entries:
    for name in list(df.columns):
        if name not in ["Código do fundo", "Setor"] and pd.api.types.is_string_dtype(df[name]):
            df = make_numeric(df, name)
    print(df.info())
    return df