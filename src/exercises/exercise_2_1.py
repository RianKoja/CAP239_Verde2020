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


def run(country_objs, report):
    report.add_heading("Cullen-Frey charts for each time series", level=3)
    country_list = [data.country for data in country_objs]
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index']:
            report.add_heading("Cullen-Frey for " + var, level=4)
            skews = list()
            kurt = list()
            for obj in country_objs:
                var_list = obj.df[var].to_list()
                skews.append(skew(var_list))
                kurt.append(kurtosis(var_list, fisher=False))

            cullen_frey_giovanni.cullenfrey(skews, kurt, country_list, var.replace("_", " ").title())
            report.add_fig()


if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    objs_list = [getdata.CountryData(country=country) for country in ["Brazil", "Italy"]]
    run(objs_list, doc)
    plt.show()
