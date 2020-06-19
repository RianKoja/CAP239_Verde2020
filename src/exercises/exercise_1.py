
# Standard imports:
import matplotlib.pyplot as plt

# Custom imports:
from tools import getdata, createdocument


def run(country_objs, report):
    report.add_heading("Item 1", level=2)
    report.add_heading("Time Series Plots", level=3)
    report.add_paragraph("Here we plot the time series charts for the variables under investigation.")
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index']:
            report.add_heading("Plot for " + var, level=4)
            ax = None
            for obj in country_objs:
                if ax is None:
                    ax = obj.df.plot(x='date', y=var, label=obj.location)
                else:
                    obj.df.plot(x='date', y=var, label=obj.location, ax=ax)
            plt.grid('both')
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.title('Time series of ' + var.replace("_", " ").title() + ' for selected countries')
            plt.tight_layout()
            plt.draw()
            report.add_fig()


if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    objs_list = [getdata.CovidData(country=country) for country in ["Brazil", "Italy"]]
    run(objs_list, doc)
    plt.show()

