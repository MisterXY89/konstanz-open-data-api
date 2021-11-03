import pandas as pd
import xlrd

class xlsFetcher(object):
    """
    xlsFetcher: fetches xls files
    """

    def __init__(self):
        self.flag_final = True

    def parse_xls(self, url):
        """
        parses data from url to dataframe

        PARAMETERS:
        -----------
        url: String
            data id based link

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
        function to load data set

        PARAMETERS:
	    -----------
        url: String
			data id based link

        RETURNS:
	    -----------
        DataFrame: data for url
        Boolean: flag_final (true if success)
        """
        return self.parse_xls(url), self.flag_final
