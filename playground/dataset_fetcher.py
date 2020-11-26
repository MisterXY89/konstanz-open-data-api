
import os
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
		try:
			data_frame = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)
			data_frame.fetched = os.path.getmtime(CURRENT_PACKAGE_LIST_FILE)
			return data_frame
		except Exception as e:
			print(e)
			return False

	def fetch_dataset_urls(self, p_id):
		response = requests.get(PACKAGE_BASE_URL + p_id) # , header=
		if response.status_code == 200:
			resources = response.json()["result"][0]["resources"]
			for resource in resources:
				yield resource["url"], resource["name"], resource["format"]
		return response.status_code

	def parse_csv(self, url, encoding="gbk", flag=False):
		try:
			return pd.read_csv(url, sep=self.seperator, encoding=encoding, error_bad_lines=False)
		except Exception as read_error:
			if not flag and isinstance(read_error, UnicodeDecodeError):
				return self.parse_csv(url, encoding='gbk', flag=True)
			return False

	def verify_url(self, url):
		"""
		check if an url belongs to offene-daten-konstanz.de
		"""
		return "offenedaten-konstanz.de" in url

	def load_data(self, p_id):
		print(f"Loading data for {p_id=}\n")
		for url, title, format in self.fetch_dataset_urls(p_id):
			if self.verify_url(url):
				df = self.parse_csv(url)
				print(f"> Successfully read data for dataset '{title}':\n> {url}")
			else:
				print(f"> 3rd-Party Url/Dataset detected for '{title}' and therefore skipped:\n> {url}")
			print("----")




p_id = "6ebde3b5-333e-4d94-85f7-d37763493b8c"

dsf = DataSetFetcher()
generator = dsf.load_data(p_id)
#
# print(next(generator))
