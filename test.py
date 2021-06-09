from opencity import config as conf 
from opencity import opencity as oc

cf = conf.Config(PKG_FOLDER="/Users/silkehusse/Documents/CorrelAid/konstanz-open-data-api/opencity")
open_city = oc.OpenCity(cf=cf)
#open_city = oc.OpenCity()

#open_city = oc.OpenCity()

open_city.get_data(["Politik und Wahlen"], tag = True, meta = True)

#open_city.show_data()
#open_city.show_data(overview=True)


res = open_city.get_data(["oeffentliche_papiereimer"])
# print(res)
# print(type(res))
# res = open_city.save_data(["parkplaetze"], folder="test_folder/")
# print(res)
