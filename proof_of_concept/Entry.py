########################################################################################################################
# Entry file to run analysis on a table of financial indicators for Brazilian real state funds.
#
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
########################################################################################################################

# Standard Imports:
import matplotlib.pyplot as plt
import seaborn as sns

# Local imports:
import code.getdata as getdata
import code.plotlist as plotlist

#  Not sure why this is required:
sns.set(style='ticks')

#  define the source of data:
xlsx_name = 'Funds16Nov2019.xlsx'

#  Read the csv file:
xls_df = getdata.acquire_data(xlsx_name)

# Show data for debug/curiosity:
print("Categorias:")
print(xls_df["Setor"].unique())

#Use separate file to decide which graphs to actually plot:
plotlist.makeplots(xls_df, xlsx_name)

input("Press enter to close all and quit")

print("Finished " + __file__)
