
# import os
# from config import *
from pandas import pandas as pd
from basic_fetcher import BasicFetcher

class csvFetcher(BasicFetcher):
	"""
	csvFetcher. fetches csv Data 
	"""
	def __init__(self):
		self.flag_final = False
		self.fallback_seperator = ";"

	def verify_df(self, df1, url, encoding, sep):
		"""
		INPUT: 
		df1:

		url: Data ID based link

		encoding

		sep:

		OUTPUT: 
		Boolean 
		"""
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
		"""
		parses data from url to dataframe 

		INPUT:
		url: Data ID based link 

		encoding:

		det_flag: 

		decode_flag: 

		sep:

		OUTPUT:
		data as pandas DataFrame, object 
		"""
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
				self.flag_final = True
				return df
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
		"""
        function to load the data 

        INPUT:
        url: Data ID based link

        OUTPUT: 
        data as a pandas DataFrame object 
        flag_final 
        """
		return self.parse_csv(url), self.flag_final