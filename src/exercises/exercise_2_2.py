########################################################################################################################
# Plot Probability Density Functions for Time series.
#
#
# Written by Renato Branco and adapted by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard imports:
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

# Local imports:
from tools import getdata, createdocument, cullen_frey_giovanni
from tools import stat, plot_ajuste
            
            
def run(country_objs, report):
    report.add_heading("Estimating Probability Density Functions", level=3)
    country_list = [data.location for data in country_objs]
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index', 'total_deaths', 'total_cases']:
            # Add title for info to be analyzed:
            report.add_heading("Data Type: " + var, level=4)
            # run for countries to group graphs by country and data type:
            for obj in country_objs:
                sinal = obj.df[var].to_list()
                plot_ajuste.plotajuste_completo(sinal, 30, var+" PDF Adjustment \n"+obj.location)
                plt.grid('both')
                plt.legend()
                report.add_fig()
                plot_ajuste.plothistograma(sinal, 30, var+" Histogram \n"+obj.location)
                plt.grid('both')
                report.add_fig()
                
                plt.close("all")


if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    data_objs = [getdata.CovidData(country=country) for country in ["Brazil", "Italy"]]
    run(data_objs, doc)
    
    doc.finish()
    
    plt.show()

