# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 12:00:00 2020

@author: Denis Eiras

Exercício 5 do trabalho
"""

import matplotlib.pyplot as plt

# Local imports:
from tools import getdata, createdocument, series_tools, soc_plot


def run_plot_and_soc(country_objs, columns, points_in_series_num, report):
    for ct in country_objs:
        print("Days for {} = {}".format(ct.country, ct.df.size))

    for column in columns:
        title = "Serie plot of {} in days".format(column.capitalize())
        report.add_heading(title, level=4)
        soc_plot.init_plot()
        for country_obj in country_objs:
            country_values = country_obj.df[column].to_list()
            plt.plot(range(len(country_values)), country_values, label=country_obj.country)
            plt.title(title)
            plt.xlabel('days')
            plt.ylabel(column.capitalize())
            plt.legend()
        plt.draw()
        report.add_fig()

        title = "Serie plot of {} in hours".format(column.capitalize())
        report.add_heading(title, level=4)
        soc_plot.init_plot()
        dic_country_time = {}
        for country_obj in country_objs:
            df_country_time = series_tools.generate_values_in_serie(country_obj.df, [column], points_in_series_num,
                                                                    is_random=True)
            list_points_in_series = df_country_time[column].to_list()
            dic_country_time[country_obj.country] = list_points_in_series
            plt.plot(range(len(list_points_in_series)), list_points_in_series, label=country_obj.country)
            plt.title(title)
            plt.xlabel('hours')
            plt.ylabel(column)
            plt.legend()
            plt.draw()
        report.add_fig()

        title = "SOC plot of {} in days".format(column.capitalize())
        report.add_heading(title, level=4)
        soc_plot.init_plot()
        for country_obj in country_objs:
            try:
                soc_plot.addplot(country_obj.df[column].to_list(), country_obj.country)
            except Exception as e:
                print(e)
                pass
        soc_plot.plot(title)
        report.add_fig()

        title = "SOC plot of {} suspects in hours".format(column.capitalize())
        report.add_heading(title, level=4)
        soc_plot.init_plot()
        for country_obj in country_objs:
            try:
                soc_plot.addplot(dic_country_time[country_obj.country], country_obj.country)
            except Exception as e:
                print(e)
                pass
        soc_plot.plot(title)
        report.add_fig()


def run(country_objs_, columns, report, date_ini, date_end, points_betw_days):
    title = "SOC Series and plot of {} for all countries. Date from {} to {}".format(', '.join(columns),
                                                                                     date_ini, date_end)
    report.add_heading(title, level=3)
    country_objs = country_objs_.copy()
    for country in country_objs:
        country.df = getdata.acquire_data(country.country, date_ini=date_ini, date_end=date_end, is_drop_na=False,
                                          start_after_new_cases=0)
    run_plot_and_soc(country_objs, columns, points_betw_days, report)


if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    country_list = ["Brazil", "Italy"]
    country_objs = [getdata.CountryData(country=country, auto_aquire_data=False) for country in country_list]
    run(country_objs, ['new_cases', 'new_deaths', 'new_tests'], doc, '2020-03-18', '2020-06-05', 23)
    doc.finish()
    print("Finished ", __file__)
