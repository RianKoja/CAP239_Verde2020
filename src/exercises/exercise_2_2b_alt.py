#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 20:34:53 2020

@author: renato
"""


# Standard imports:
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
from statistics import variance
from scipy.interpolate import interp1d

# Local imports:
from tools import getdata, createdocument
from tools import kmeans_silhouette
import pandas as pd

            
def run(country_objs, report):
    report.add_heading("K-Means clustering based on statistical parameters", level=3)
    parameters = ['var', 'skew', 'kurt']
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index', 'new_tests']:
            stat_df = pd.DataFrame()  # df for the statistical moments
            
            # Add heading about information analyzed:
            report.add_heading("Data Type: " + var, level=4)
            # Iterate over countries:
            for obj in country_objs:
                # Compute Variance, skewness and Kurtosis
                sinal = obj.df[var].to_list()
                mapper = interp1d([min(sinal), max(sinal)], [0, 1])
                sinal_norm = mapper(sinal)
                
                # statistical moments for the normalized signal
                vari = variance(sinal_norm)
                assi = skew(sinal_norm)
                curt = kurtosis(sinal_norm, fisher=False)
                
                df_aux = pd.DataFrame([[vari, assi, curt]], columns=parameters)
                stat_df = stat_df.append(df_aux, ignore_index=True, sort=False)
            
            vari = stat_df['var'].to_list()
            assi = stat_df['skew'].to_list()
            curt = stat_df['kurt'].to_list()
            # normalized statistics moments
            mapper = interp1d([min(vari), max(vari)], [0, 1])
            vari_norm = mapper(vari) 
            mapper = interp1d([min(assi), max(assi)], [0, 1])
            assi_norm = mapper(assi) 
            mapper = interp1d([min(curt), max(curt)], [0, 1])
            curt_norm = mapper(curt) 

            stat_df_norm = pd.DataFrame()
            stat_df_norm['var'] = vari_norm
            stat_df_norm['skew'] = assi_norm
            stat_df_norm['kurt'] = curt_norm
            
            # plot the K-Means for the normalized signal
            kmeans_silhouette.plot_k_means(stat_df, parameters, report, var + " - Normalized Signal")
            
            # plot the K-Means for the normalized statistical moments
            kmeans_silhouette.plot_k_means(stat_df_norm, parameters, report, var + " - Normalized Stastistical Moments")

            plt.close("all")
            

if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China",
                    "South Korea"]
    obj_list = [getdata.CovidData(country=country) for country in country_list]
    run(obj_list, doc)
    
    doc.finish()
    
    plt.show()
