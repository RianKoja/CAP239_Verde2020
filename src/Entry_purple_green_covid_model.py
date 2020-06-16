########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

# Local imports:
from tools import createdocument  # , cullen_frey_giovanni, getdata
from tools.covid_model_data import get_dados_covid_por_agrupador, CovidModelConfig
from purple_green_covid_model.covid_model_core import run, plot_g_s


print("Started ", __file__)

report = createdocument.ReportDocument()
report.add_heading("Building the Data-Set", level=2)

country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China", "South Korea"]
prob_agents_spec = {'Espectro 1': [0.5, 0.45, 0.05], 'Espectro 2': [0.7, 0.25, 0.05]}

for country in country_list:
    for prob_key, prob_val in prob_agents_spec.items():
        prob_dic_one = {prob_key: prob_val}
        report.add_heading("Prediction for " + country)

        cfg = CovidModelConfig(country, '2020-05-20', '2020-06-16', '2020-05-27', prob_agents=prob_dic_one)
        cfg.estrategia_n8 = 'UpDown'
        df = get_dados_covid_por_agrupador(cfg)
        g, s, n_k, n_k_real = run(cfg, df)
        report.add_fig()

        report.add_heading("Factor g and s for " + country)
        plot_g_s(cfg, g, s, n_k_real)
        report.add_fig()

report.finish()

print("Finished ", __file__)
