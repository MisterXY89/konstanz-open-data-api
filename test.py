# from opencity import config as conf 
from opencity import opencity as oc

# cf = conf.Config(PKG_FOLDER="/home/dragonfly")
# open_city = oc.OpenCity(cf=cf)

open_city = oc.OpenCity()


open_city.show_data()
open_city.show_data(overview=True)

# res = open_city.get_data("parkplaetze")
# print(res)