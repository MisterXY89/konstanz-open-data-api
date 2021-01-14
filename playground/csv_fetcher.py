
# import os
# from config import *
from pandas import pandas as pd
from basic_fetcher import BasicFetcher

class CSVFetcher(BasicFetcher):
	"""
	docstring for DataSetFetcher
	"""
	def __init__(self):
		super(CSVFetcher, self).__init__()
		self.fallback_seperator = ";"

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


	def parse_csv(self, url, encoding="utf-8", det_flag=False, decode_flag=False, sep=";"):
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
				return df, True
			raise Exception("SeperatorException: expected after")
		except Exception as read_error:
			print(40*"#")
			print(read_error)
			print(40*"#")
			if not decode_flag and isinstance(read_error, UnicodeDecodeError):
				# iso-8859-1
				return self.parse_csv(url, encoding='latin1', decode_flag=True, sep=sep)
			if not det_flag and "expected" in str(read_error).lower():
				return self.parse_csv(url, encoding=encoding, det_flag=True, sep=",")
			return None, False


	def load_data(self, url):
		#print(f"Loading data for {p_id=}\n")
		#for url, title, format in self.fetch_dataset_urls(p_id):
		#	if self.verify_url(url) and self.get_file_ending(url) == "csv":
		return self.parse_csv(url)
				#print(df)
				#print(f"> Successfully read data for dataset '{title}':\n> {url}")
			#else:
				#print(f"> 3rd-Party Url/Dataset detected for and therefore skipped:\n> {url}")
			#print("----")



#
# p_id = "6ebde3b5-333e-4d94-85f7-d37763493b8c"
#
dsf = CSVFetcher()
gen = dsf.fetch_resource_urls("1fd6d20a-44c5-4dc8-994f-305a723e5511")
#print(next(gen))
#print(next(gen))
#print(next(gen))

# generator = dsf.load_data(p_id)
#
# print(next(generator))
