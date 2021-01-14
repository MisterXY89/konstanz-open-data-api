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

        INPUT:
        url: Data ID based link

        OUTPUT:
        data as pandas DataFrame object
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

        INPUT:
        url: Data ID based link

        OUPUT: 
        data as a pandas DataFrame object
        flag_final
        """
        return self.parse_xls(url), self.flag_final
