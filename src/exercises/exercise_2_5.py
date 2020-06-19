# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:47:02 2020

@author: Giovanni Guarnieri Soares
"""


# Standard imports:
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import curve_fit


# Local imports:
from tools import getdata


class PlaceHolderDoc:
    def __init__(self):
        pass

    def add_fig(self):
        pass

    def add_paragraph(self, txt):
        pass

    def add_heading(self, txt, level=2):
        pass


# Used to fit an exponential:
def func(x, a, c, d):
    return a*np.exp(-c*x)+d


def run(countrylist, doc=PlaceHolderDoc()):
    doc.add_heading("Regression Analysis for Tests and Cases", level=3)
    doc.add_paragraph("Not all countries have provided their daily and total test statistics, empty plots may be " +
                      "shown for this case.")
    countrylist.sort()
    for country in countrylist:
        doc.add_heading(country, level=4)
        df = getdata.acquire_data(country, acquire_tests=True)
        plt.figure()
        plt.xlabel("New Daily Cases")
        plt.grid("both")
        plt.ylabel("New Daily Tests")
        plt.plot(df['new_cases'], df['new_tests'], 'o', label="Data")
        try:
            m1 = [int(max(df['new_tests'])), int(max(df['new_cases']))]
            plt.plot(range(min(m1)), range(min(m1)), label="y=x", linestyle='--')
            x_regression = df['new_cases'].to_list()
            slope, intercept, rvalue, pvalue, stderr = linregress(x_regression, df['new_tests'].to_list())
            x_regression = [0] + x_regression
            y_regression = [intercept + slope * x for x in x_regression]
            plt.plot(x_regression, y_regression, label="regression")
            plt.title(country + "\n" + 'Regression: y = {:.4f} x + {:.4f}'.format(slope, intercept) + "\n" +
                      'Correlation Coefficient: {:.4f}  Standard Error: {:.4f}'.format(rvalue, stderr))
        except:
            plt.title(country)

        plt.legend()

        plt.draw()
        doc.add_fig()

        plt.figure()
        plt.plot(df['total_cases'], df['total_tests'], 'o', label="Data")
        try:
            m1 = [int(max(df['total_tests'])), int(max(df['total_cases']))]
            plt.plot(range(min(m1)), range(min(m1)), label="y=x", linestyle='--')
            popt, pcov = curve_fit(func, df['total_cases'].to_list(), df['total_tests'].to_list(), p0=(1, 1e-6, 1))
            diag_cov = np.diag(pcov)
            y_exp = func(np.asarray(df['total_cases'].to_list()), popt[0], popt[1], popt[2])
            plt.plot(df['total_cases'].to_list(), y_exp, label='Regression')
            plt.title(
                country + "\n" + 'Regression: y = {:.4f} exp (-{:.4g} x) + {:.4f}'.format(popt[0], -popt[1], popt[2]) +
                "\n" + 'Fit covariances: {:.4f} | {:.4g} | {:.4f}'.format(diag_cov[0], diag_cov[1], diag_cov[2]))
        except:
            plt.title(country)

        plt.legend()
        plt.xlabel("Total Cases")
        plt.grid("both")
        plt.ylabel("Total Tests")
        plt.draw()
        doc.add_fig()


if __name__ == '__main__':
    run(["Italy", "Belgium", "South Korea"])
    plt.show()
