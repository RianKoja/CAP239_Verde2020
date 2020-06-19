# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 17:51:03 2020

@author: Giovanni Guarnieri Soares
"""

import matplotlib.pyplot as plt

from tools import imcsf_covid_19, getdata, createdocument


def run(country_objs, doc):
    for obj in country_objs:
        imcsf_covid_19.make_predict(obj.df["new_cases"].to_list(), obj.location, savegraphs=False, doc=doc)


if __name__ == '__main__':
    countries = ["Brazil", "Italy"]
    obj_list = [getdata.CovidData(country=country) for country in countries]
    report = createdocument.ReportDocument()
    run(obj_list, report)
    report.finish()
    plt.show()
