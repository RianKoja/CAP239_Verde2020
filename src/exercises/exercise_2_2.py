########################################################################################################################
# Create Cullen-Frey chart to compare COVID-19 data series in different countries and add them to a docx report.
#
#
# Written by Rian Koja and Giovani Guarnieri to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard imports:
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

# Local imports:
from tools import getdata, createdocument, cullen_frey_giovanni
from tools import stat, plot_ajuste
            
            
def run(country_objs, report):
    country_list = [data.country for data in country_objs]    
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index', 'new_tests']:
            #adicionar o título do tipo de informação analisada
            report.add_heading("Data Type: " + var)
            #corre os países para agrupar os gráficos dos países por coluna analisada
            for obj in country_objs:
                sinal = obj.df[var].to_list()
                #sinal = country_objs[i][var].to_list()
                plot_ajuste.plotajuste_completo(sinal, 30, var+" PDF Adjustment \n"+obj.country)
                report.add_fig()
                plot_ajuste.plothistograma(sinal, 30, var+" Histogram \n"+obj.country)
                report.add_fig()
                
                plt.close("all")
            
            

    

if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    country_objs = [getdata.CountryData(country=country) for country in ["Brazil", "Italy"]]
    run(country_objs, doc)
    
    doc.finish()
    
    plt.show()
    
    
