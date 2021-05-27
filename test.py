from opencity import config as conf 
from opencity import opencity as oc

cf = conf.Config(PKG_FOLDER="/Users/silkehusse/Documents/CorrelAid/konstanz-open-data-api/opencity")
open_city = oc.OpenCity(cf=cf)

#open_city = oc.OpenCity()

open_city.get_data(["oeffentliche_papiereimer"])

#open_city.show_data()
#open_city.show_data(overview=True)

# res = open_city.get_data("parkplaetze")
# print(res)