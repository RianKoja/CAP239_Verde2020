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


def run(country_list, report):
    country_df_list = [getdata.acquire_data(country=country) for country in country_list]
    for var in country_df_list[0].columns:
        if var not in ['date', 'index']:
            report.add_heading("Cullen-Frey for " + var)
            skews = list()
            kurt = list()
            for df in country_df_list:
                var_list = df[var].to_list()
                skews.append(skew(var_list))
                kurt.append(kurtosis(var_list, fisher=False))

            cullen_frey_giovanni.cullenfrey(skews, kurt, country_list, var)
            report.add_fig()


if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    run(["Brazil", "Italy"], doc)
    plt.show()
