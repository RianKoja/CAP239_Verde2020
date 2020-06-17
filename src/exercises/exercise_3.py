# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 17:51:03 2020

@author: Giovanni Guarnieri Soares
"""

from tools import IMCSF_Covid_19, getdata

def run(country_list, doc):
    country_list.sort()
    for country in country_list:
        df=getdata.acquire_data(country)
        IMCSF_Covid_19.makePredict(df["new_cases"], country, savegraphs=False, doc)
