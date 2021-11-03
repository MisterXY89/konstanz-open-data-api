import json
import requests
from pandas import pandas as pd
import geopandas as gpd

class shpFetcher:
    """
    shpFetcher: fetches GeoData
    """

    def __init__(self):
        self.flag_final = True

    def parse_geo(self, url):
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
            df = gpd.read_file(url)
            return df
        except:
            self.flag_final = False
            return gpd.GeoDataFrame()

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
        return self.parse_geo(url), self.flag_final
