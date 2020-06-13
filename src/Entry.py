########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

# Local imports:
from tools import createdocument, cullen_frey_giovanni, getdata

print("Started ", __file__)

report = createdocument.ReportDocument()

report.add_heading("Building the Data-Set", level=2)
country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium"]
for country in country_list:
    report.add_heading("Cullen-Frey for " + country)
    df = getdata.acquire_data(country=country)
    print(df.columns)
    for var in df.columns:
        if var != 'date':
            print(var)
            var_list = df[var].to_list()
            print(var_list)
            print(type(var_list))
            cullen_frey_giovanni.cullenfrey_from_data(var_list, country, var)
            report.add_fig()


report.finish()

print("Finished ", __file__)
