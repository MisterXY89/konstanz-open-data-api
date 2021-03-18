
# import os
from pandas import pandas as pd
from .basic_fetcher import BasicFetcher

class csvFetcher(BasicFetcher):
	"""
	csvFetcher
	inherits basic fetcher
	"""
	def __init__(self):
		self.flag_final = False
		self.fallback_seperator = ";"

	def verify_df(self, df1, url, encoding, sep):
		"""
		checkf if csv has been correctly read into dataframe
		-> avoid issues

		PARA METERS:
	    -----------
		df1: Dataframe
			current df1
		url: String
			data ID based link
		encoding: String
			encoding for csv file
		sep: String
			csv file seperator

		RETURNS:
	    -----------
		Boolean: if dataframe is created correctly
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
				#print("+++ False")
				return False
		except:
			pass
			#print("*** TRUE")
		return True


	def parse_csv(self, url, encoding="utf-8", det_flag=False, decode_flag=False, sep=";"):
		"""
		parses data from url to dataframe

		PARAMETERS:
	    -----------
		url: String
			Data ID based link
		encoding: String
			default: 'utf-8'
			encoding for csv file
		det_flag: Boolean
			default: False
			control max number of repetitions
		decode_flag: Boolean
			default: False
			track if another encoding has been tried
		sep: String
			default: ';'
			csv file seperator

		RETURNS:
	    -----------
		DataFrame: data for url
        Boolean: flag_final (success)
		"""
		try:
			df = pd.read_csv(url, sep=sep,
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
			if not decode_flag and isinstance(read_error, UnicodeDecodeError):
				# iso-8859-1
				return self.parse_csv(url, encoding='latin1', decode_flag=True, sep=sep)
			if not det_flag and "expected" in str(read_error).lower():
				return self.parse_csv(url, encoding=encoding, det_flag=True, sep=",")
			return None, False


	def load_data(self, url):
		"""
        function to load the data

        PARAMETERS:
	    -----------
        url: String
			Data ID based link

        RETURNS:
	    -----------
        DataFrame: data for url
        Boolean: flag_final (success)
        """
		return self.parse_csv(url), self.flag_final
