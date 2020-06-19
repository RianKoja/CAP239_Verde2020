########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

# Local imports:
from tools import createdocument, getdata
from exercises import exercise_1, exercise_2_1, exercise_2_2, exercise_2_2b_alt, exercise_2_5
from exercises import exercise_2_x, exercise_3, exercise_4, exercise_5


print("Started ", __file__)

# Preparing variables:
report = createdocument.ReportDocument()
country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China", "South Korea"]
brazilian_states = ['AM', 'CE']
country_objs = [getdata.CovidData(country=country) for country in country_list]
state_objs = [getdata.CovidData(brazil_state=state) for state in brazilian_states]
favela_objs = [getdata.CovidData()]
data_objs = country_objs + state_objs + favela_objs

# Plot time series:
exercise_1.run(data_objs, report)

report.add_heading("Item 2", level=2)
# Add cullen-Frey charts:
exercise_2_1.run(data_objs, report)

exercise_2_2.run(data_objs, report)
# exercise_2_2b.run(country_objs, report)
exercise_2_2b_alt.run(country_objs, report)
# exercise_2_2c.run(country_objs, report)
# exercise_2_2d.run(country_objs, report)
# Add NDC x NDT graphs
exercise_2_5.run(country_list, report)
# Check for multi-fractality properties:
exercise_2_x.run(data_objs, report)

# Add ICMSF-Covid-19 predictions:
report.add_heading("Item 3", level=2)
exercise_3.run(data_objs, doc=report)

# Add Modified-ICMSF-Covid-19 predictions:
report.add_heading("Item 4", level=2)
exercise_4.run(data_objs, doc=report)

# SOC in days and hours
report.add_heading("Item 5", level=2)
exercise_5.run(report, '2020-03-18', '2020-06-05', 23, country_list)

report.finish()

print("Finished ", __file__)
