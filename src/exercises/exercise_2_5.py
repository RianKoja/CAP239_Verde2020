# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:47:02 2020

@author: Giovanni Guarnieri Soares
"""


# Standard imports:
from tools import getdata
import matplotlib.pyplot as plt


def run(countrylist, doc=None):
    countrylist.sort()
    for country in countrylist:
        df = getdata.acquire_data(country, include_tests=True)
        plt.figure()
        plt.xlabel("New Daily Cases")
        plt.grid("both")
        plt.ylabel("New Daily Tests")
        plt.title(country)
        plt.plot(df['new_cases'], df['new_tests'], 'o', label="Data")
        try:
            m1 = [int(max(df['new_tests'])), int(max(df['new_cases']))]
            plt.plot(range(min(m1)), range(min(m1)), label="y=x")
        except:
            print("no tests\n")
        plt.draw()
        if doc is None:
            plt.show()
        else:
            doc.add_fig()
