
import os
import requests
from config import *
from io import StringIO
from pandas import pandas as pd
#from detect_delimiter import detect

class csvFetcher:
	"""
	docstring for DataSetFetcher
	"""
	def __init__(self):
		self.fallback_seperator = ";"

	def fetch_dataset_urls(self, p_id):
		response = requests.get(PACKAGE_BASE_URL + p_id) # , header=
		if response.status_code == 200:
			resources = response.json()["result"][0]["resources"]
			for resource in resources:
				yield resource["url"], resource["name"], resource["format"]
		return response.status_code


	def verify_df(self, df1, url, encoding, sep):
		try:
			anti_sep = "," if sep == ";" else ";"
			df2 = pd.read_table(url, sep=anti_sep,
									encoding=encoding,
									engine="python",
									keep_default_na=False,
									skip_blank_lines=True
									)
			if len(list(df2.columns)) > len(list(df1.columns)):
				print("+++ False")
				return False
		except:
			print("*** TRUE")
		return True


	def parse_csv(self, url, encoding="iso-8859-1", det_flag=False, decode_flag=False, sep=";"):
		try:
			df = pd.read_table(url, sep=sep,
									encoding=encoding,
									engine="python",
									keep_default_na=False,
									skip_blank_lines=True
									# error_bad_lines=True,
									# decimal=",",
									# quotechar='"',
									)
			if self.verify_df(df, url, encoding, sep):
				return df
			raise Exception("SeperatorExpection: expected after")
		except Exception as read_error:
			print(read_error)
			if not decode_flag and isinstance(read_error, UnicodeDecodeError):
				# iso-8859-1
				return self.parse_csv(url, encoding='latin1', decode_flag=True, sep=sep)
			if not det_flag and "expected after" in str(read_error):
				return self.parse_csv(url, encoding=encoding, det_flag=True, sep=",")
			return False

	def verify_url(self, url):
		"""
		check if an url belongs to offene-daten-konstanz.de
		"""
		return "offenedaten-konstanz.de" in url

	def get_file_ending(self, url):
		"""
		extract file ending from an url
		"""
		return url.split(".")[::-1][0]

	def load_data(self, url):
		#print(f"Loading data for {p_id=}\n")
		#for url, title, format in self.fetch_dataset_urls(p_id):
		#	if self.verify_url(url) and self.get_file_ending(url) == "csv":
		return self.parse_csv(url), True
				#print(df)
				#print(f"> Successfully read data for dataset '{title}':\n> {url}")
			#else:
				#print(f"> 3rd-Party Url/Dataset detected for and therefore skipped:\n> {url}")
			#print("----")



#
# p_id = "6ebde3b5-333e-4d94-85f7-d37763493b8c"
#
# dsf = CSVFetcher()
# generator = dsf.load_data(p_id)
#
# print(next(generator))
