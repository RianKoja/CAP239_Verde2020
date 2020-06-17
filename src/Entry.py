########################################################################################################################
# Call functions and organize report.
#
########################################################################################################################

# Local imports:
from tools import createdocument, cullen_frey_giovanni, getdata
from exercises import exercise_2_1


print("Started ", __file__)

report = createdocument.ReportDocument()

report.add_heading("Building the Data-Set", level=2)
country_list = ["Brazil", "Portugal", "Spain", "France", "Belgium", "United States", "Italy", "China", "South Korea"]

# Add cullen-Frey charts:
exercise_2_1.run(country_list, report)
# Add ICMSF-Covid-19 predictions:
exercise_3.makePredict(df["new_cases"], country, doc=report)

# Add Modified-ICMSF-Covid-19 predictions:
exercise_4.makePredict_v2(df["new_cases"], country, doc=report)

report.finish()

print("Finished ", __file__)
