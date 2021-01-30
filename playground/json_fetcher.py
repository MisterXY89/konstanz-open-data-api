import pandas as pd


class jsonFetcher(object):
    """
    jsonFetcher: fetches json-Data
    """

    def __init__(self):
        self.flag_final = True

    def parse_json(self, url):
        """
        parses data from url to dataframe 

        INPUT:
        url: Data ID based link

        OUTPUT:
        data as pandas DataFrame object
        """
        try:
            df = pd.read_json(url)
            # TO DO : different encodings
            return df
        except:
            self.flag_final = False
            return pd.DataFrame()

    def load_data(self, url):
        """
        load data set

        INPUT:
        url: Data ID based link

        OUTPUT: 
        data as a pandas DataFrame object 
        flag_final 
        """
        return self.parse_json(url), self.flag_final

