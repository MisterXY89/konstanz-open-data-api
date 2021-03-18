
import pandas as pd
import xlrd

class xlsFetcher(object):
    """
    xlsFetcher: fetces xls-Data
    """

    def __init__(self):
        self.flag_final = True

    def parse_xls(self, url):
        """
        parses data from url to dataframe

        PARAMETERS:
        -----------
        url: String
            Data ID based link

        RETURNS:
	    -----------
        DataFrame: data for url
        """
        try:
            df = pd.read_excel(url, sheet_name=None)
            return df
        except:
            self.flag_final = False
            return pd.DataFrame()

    def load_data(self, url):
        """
        load data set

        PARAMETERS:
	    -----------
        url: String
			Data ID based link

        RETURNS:
	    -----------
        DataFrame: data for url
        Boolean: flag_final (success)
        """
        return self.parse_xls(url), self.flag_final
