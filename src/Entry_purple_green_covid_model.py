########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

from purple_green_covid_model.covid_model_core import run, plot_g_s
from purple_green_covid_model.covid_model_data import get_dados_covid_por_agrupador, CovidModelConfig
# Local imports:
from tools import createdocument, soc_plot

print("Started ", __file__)

green_list = ["Brazil", "Portugal", "Spain", "France", "Belgium", ]
purple_list = ["Brazil", "United States", "Italy", "China", "South Korea"]
prob_agents_spec = {'Espectro 1': [0.5, 0.45, 0.05], 'Espectro 2': [0.7, 0.25, 0.05]}
wanted_columns = ['new_cases']
random_lines_between_lines_num = 23
dic_list = {'Green': green_list, 'Purple': purple_list}

for list_name, country_list in dic_list.items():

    report = createdocument.ReportDocument()
    report.add_heading("{} country list".format(list_name), level=2)

    dic_country_nk = {}
    dic_country_nk_time = {}
    for prob_key, prob_val in prob_agents_spec.items():
        for country in country_list:
            prob_dic_one = {prob_key: prob_val}

            report.add_heading("Prediction for {} in days".format(country))
            cfg = CovidModelConfig(country, '2020-04-20', '2020-05-17', '2020-04-27', prob_agents=prob_dic_one)
            cfg.estrategia_n8 = 'UpDown'
            df = get_dados_covid_por_agrupador(cfg)

            # run for data serie in days (owid original)
            g, s, n_k, n_k_real = run(cfg, df)
            dic_country_nk[country] = n_k
            report.add_fig()

            report.add_heading("Prediction for {} in hours".format(country))
            g_time, s_time, n_k_time, n_k_real_time = run(cfg, df, random_lines_between_lines_num)
            dic_country_nk_time[country] = n_k_time
            report.add_fig()

            report.add_heading("Factor g and s for {}. First in days, then hours".format(country))
            plot_g_s(cfg, g, s, n_k_real)
            report.add_fig()
            plot_g_s(cfg, g_time, s_time, n_k_real_time)
            report.add_fig()

        # SOC for countries
        soc_title = "SOC plot for {} country list. First in days, then hours".format(list_name)
        report.add_heading(soc_title)
        soc_plot.init_plot()
        for country, n_k_item in dic_country_nk.items():
            try:
                soc_plot.addplot(n_k_item, country)
            except Exception as e:
                pass
        soc_plot.plot(soc_title)
        report.add_fig()

        soc_plot.init_plot()
        for country, n_k_item in dic_country_nk_time.items():
            try:
                soc_plot.addplot(n_k_item, country)
            except Exception as e:
                pass
        soc_plot.plot(soc_title)
        report.add_fig()

    report.finish()

print("Finished ", __file__)
