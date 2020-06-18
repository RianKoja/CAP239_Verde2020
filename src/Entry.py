########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

from exercises import exercise_2_1, exercise_3, exercise_5
# Local imports:
from tools import createdocument, getdata

print("Started ", __file__)

report = createdocument.ReportDocument()

report.add_heading("Building the Data-Set", level=2)
country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China", "South Korea"]
country_objs = [getdata.CountryData(country=country) for country in country_list]

# Add cullen-Frey charts:
exercise_2_1.run(country_objs, report)

# exercise_2_2.run(country_objs, report)
# exercise_2_2b.run(country_objs, report)
# exercise_2_2c.run(country_objs, report)
# exercise_2_2d.run(country_objs, report)

# Add ICMSF-Covid-19 predictions:
exercise_3.run(country_objs, doc=report)

# Add Modified-ICMSF-Covid-19 predictions:
# exercise_4.makePredict_v2(df["new_cases"], country, doc=report)

# SOC in days and hours
exercise_5.run(report, '2020-03-18', '2020-06-05', 23, country_list)

report.finish()

print("Finished ", __file__)
