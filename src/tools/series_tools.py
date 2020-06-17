# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 12:00:00 2020

@author: Denis Eiras

"""

import numpy as np
import pandas as pd


def generate_values_in_serie(df_serie, columns, num_of_values, is_random=True):
    num_of_values = num_of_values + 1
    df_time = pd.DataFrame()
    for index, row in df_serie.iterrows():
        # df_time = df_time.append(row.copy())
        dic_rand_cols = {}
        for column in columns:
            if is_random:
                dic_rand_cols[column] = np.random.dirichlet(np.ones(num_of_values), size=1).flatten() * row[column]
            else:
                dic_rand_cols[column] = [row[column]] * num_of_values
        for i in range(num_of_values):
            df_new_row = pd.Series()
            for column in columns:
                df_new_row[column] = dic_rand_cols[column][i]
            df_time = df_time.append(df_new_row, ignore_index=True)

    return df_time


if __name__ == '__main__':
    df = pd.DataFrame()
    sales = [{'account': 'Jones LLC', 'Jan': 150, 'Feb': 200, 'Mar': 140},
             {'account': 'Alpha Co', 'Jan': 200, 'Feb': 210, 'Mar': 215},
             {'account': 'Blue Inc', 'Jan': 50, 'Feb': 90, 'Mar': 95}]
    df = pd.DataFrame(sales)
    df = generate_values_in_serie(df, ['Jan', 'Feb', 'Mar'], 2)
    print(df)
