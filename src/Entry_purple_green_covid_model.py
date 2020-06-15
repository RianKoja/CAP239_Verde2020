########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

# Local imports:
# from tools import createdocument, cullen_frey_giovanni, getdata
from tools.covid_model_data import get_dados_covid_por_agrupador, CovidModelConfig
from purple_green_covid_model.covid_model_core import run


print("Started ", __file__)

# report = createdocument.ReportDocument()
# report.add_heading("Building the Data-Set", level=2)

country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium"]

for country in country_list:
    # report.add_heading("Prediction for " + country)

    # erxample
    cfg = CovidModelConfig(country, '2020-05-17', '2020-06-13', '2020-05-24')
    df = get_dados_covid_por_agrupador(cfg)
    run(cfg, df)
    # report.add_fig()

    # print(df.columns)
    # for var in df.columns:
    #     if var != 'date':
    #         print(var)
    #         var_list = df[var].to_list()
    #         print(var_list)
    #         print(type(var_list))
    #         cullen_frey_giovanni.cullenfrey_from_data(var_list, country, var)
    #         report.add_fig()


# report.finish()

print("Finished ", __file__)
