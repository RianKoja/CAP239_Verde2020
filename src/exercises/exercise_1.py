
# Standard imports:
import matplotlib.pyplot as plt

# Custom imports:
from tools import getdata, createdocument


def run(country_objs, report):
    report.add_heading("Time Series charts for each variable", level=3)
    country_list = [data.country for data in country_objs]
    for var in country_objs[0].df.columns:
        if var not in ['date', 'index']:
            ax = None
            for obj in country_objs:
                if ax is None:
                    ax = obj.df.plot(x='date', y=var, label=obj.country)
                else:
                    obj.df.plot(x='date', y=var, label=obj.country, ax=ax)
            plt.grid('both')
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.title('Time series of ' + var.replace("_", " ").title() + ' for selected countries')
            plt.tight_layout()
            plt.draw()
            report.add_fig()


if __name__ == "__main__":
    doc = createdocument.ReportDocument()
    objs_list = [getdata.CountryData(country=country) for country in ["Brazil", "Italy"]]
    run(objs_list, doc)
    plt.show()

