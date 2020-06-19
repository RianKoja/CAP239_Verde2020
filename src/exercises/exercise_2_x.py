import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from tools import createdocument, getdata, mfdfa_ss, print_table, specplus


def run(countries_obj, doc):
    doc.add_heading("Checking for multifractality parameters: ", level=3)
    parameters = ["country", r'$\alpha$ (DFA)', r'$\alpha_{min}$', r'$\alpha_{max}$', r'$\Delta\alpha$', r'$\alpha_0$', r'$A_\alpha$',
                  r'$\Psi$']
    for var in countries_obj[0].df.columns:
        if var not in ['date', 'index']:
            doc.add_heading("For " + var.replace("_", " ") + ":", level=4)
            xd, yd, label_list = ([], [], [])
            df_table = pd.DataFrame(columns=parameters)
            for obj in countries_obj:
                data = obj.df[var].to_list()
                stats = mfdfa_ss.main(data)
                alpha_dfa, _, _, _, _, _, = specplus.dfa1d(data, 1)
                # Save data form the last chart:
                line = plt.gca().get_lines()[0]
                xd.append(line.get_xdata())
                yd.append(line.get_ydata())
                label_list.append(obj.location)
                numbers_float = [alpha_dfa, stats['LH_min'], stats['LH_max'], stats['delta_alpha'], stats['alpha_zero'],
                                 stats['a_alpha'], stats['Psi']]
                numbers_text = ['{:.2f}'.format(x) for x in numbers_float]
                df_aux = pd.DataFrame([[obj.location] + numbers_text], columns=parameters)
                plt.close('all')
                df_table = df_table.append(df_aux, ignore_index=True, sort=False)

            plt.figure()
            for xx, yy, label in zip(xd, yd, label_list):
                plt.plot(xx, yy, '.-', label=label)
            plt.title("Comparing Singularity Spectra for " + var)
            plt.xlabel(r'$\alpha$')
            plt.ylabel(r'$f(\alpha)$')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3)
            plt.grid('on', which='both')
            plt.tight_layout()
            doc.add_fig()
            print_table.render_mpl_table(df_table, col_width=1.3, bbox=None, font_size=12)
            doc.add_fig()


if __name__ == '__main__':
    countries = ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China", "South Korea"]
    obj_list = [getdata.CovidData(country=country) for country in countries]
    report = createdocument.ReportDocument()
    run(obj_list, report)
    report.finish()
    plt.show()
