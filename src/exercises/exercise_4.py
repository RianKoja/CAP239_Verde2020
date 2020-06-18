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

from tools import IMCSF_Covid_19_modified, getdata, createdocument


def run(country_objs, doc):
    for obj in country_objs:
        IMCSF_Covid_19_modified.make_predict_v2(obj.df["new_cases"].to_list(),
                                    obj.country, doc=doc)


if __name__ == '__main__':
    countries = ["Brazil", "Italy"]
    obj_list = [getdata.CountryData(country=country) for country in countries]
    report = createdocument.ReportDocument()
    run(obj_list, report)
    report.finish()
    plt.show()
