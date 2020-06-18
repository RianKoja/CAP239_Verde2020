# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 00:15:21 2020

@author: gio-x
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 17:51:03 2020

@author: Giovanni Guarnieri Soares
"""

import matplotlib.pyplot as plt

from tools import imcsf_covid_19_modified, getdata, createdocument


def run(country_objs, doc):
    #for obj in country_objs:
    imcsf_covid_19_modified.make_predict_v2(Brazil.df["new_cases"].to_list(),
                                    "Brazil", doc=doc)


if __name__ == '__main__':
    countries = ["Brazil", "Italy"]
    obj_list = [getdata.CountryData(country=country) for country in countries]
    report = createdocument.ReportDocument()
    run(obj_list, report)
    report.finish()
    plt.show()
