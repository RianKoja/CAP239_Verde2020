########################################################################################################################
# Create Cullen-Frey chart to compare COVID-19 data series in different countries and add them to a docx report.
#
#
# Written by Rian Koja and Giovani Guarnieri to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard imports:
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
from statistics import variance
from scipy.interpolate import interp1d

# Local imports:
from tools import getdata, createdocument
from tools import elbow_yb
#import pandas as pd


def run(country_objs, report):
    # country_list = [data.country for data in country_objs]
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index', 'new_tests']:
            stat_data = []
            # adicionar o título do tipo de informação analisada
            report.add_heading("Data Type: " + var)
            # corre os países para agrupar os gráficos dos países por coluna analisada
            i_lista = 0
            for obj in country_objs:
                # Calcula Variância / Assimetria / Curtose para cada
                sinal = obj.df[var].to_list()
                mapper = interp1d([min(sinal), max(sinal)], [0, 1])
                sinal_norm = mapper(sinal)
                
                vari = variance(sinal_norm)
                assi = skew(sinal_norm)
                curt = kurtosis(sinal_norm, fisher=False)
                stat_data.append([vari, assi, curt])
                i_lista += 1
            
            country_list = [data.country for data in country_objs]
            num_k = elbow_yb.makeK(stat_data,country_list,'Elbow - '+var,report)
            print(num_k) #num_k será a entrada para a análise k-means
            report.add_fig()
                
            plt.close("all")
            
            

    

if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    country_objs = [getdata.CountryData(country=country) for country in ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China", "South Korea"]]
    run(country_objs, doc)
    
    doc.finish()
    
    plt.show()
    
    
