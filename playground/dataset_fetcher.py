
import json
import requests
from config import *
from pandas import pandas as pd

class DataSetFetcher(object):
	"""
	docstring for DataSetFetcher
	"""
	def __init__(self):
		self.seperator = ";"

	def _read_current_packages(self):
		with open(CURRENT_PACKAGE_LIST_FILE, "r") as package_list_file:
			data = package_list_file.read()
			data = json.loads(data)
			return data
		return False

	def fetch(self, p_id):
		response = requests.get(PACKAGE_BASE_URL + p_id) # , header= 
		if response.status_code == 200:
			return response.json()["result"][0]["resources"][0]["url"]
		return response.status_code

	def parseCSV(self, url):
		return pd.read_csv(url, sep=self.seperator)




p_id = "6ebde3b5-333e-4d94-85f7-d37763493b8c"


dsf = DataSetFetcher()

ds_url = dsf.fetch(p_id)
df = dsf.parseCSV(ds_url)

print(df)