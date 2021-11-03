import pandas as pd

class jsonFetcher(object):
    """
    jsonFetcher: fetch json files
    """

    def __init__(self):
        self.flag_final = True

    def parse_json(self, url):
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
            df = pd.read_json(url)
            # TO DO : different encodings
            return df
        except:
            self.flag_final = False
            return pd.DataFrame()

    def load_data(self, url):
        """
        function to load the data

        PARAMETERS:
	    -----------
        url: String
			data id based link

        RETURNS:
	    -----------
        DataFrame: data for url
        Boolean: flag_final (true if success)
        """
        return self.parse_json(url), self.flag_final
