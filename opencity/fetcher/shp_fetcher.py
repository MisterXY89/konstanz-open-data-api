import json
import requests
from pandas import pandas as pd
import geopandas as gpd  # install

class shpFetcher:
    """
    SHPFetcher: fetches GeoData
    """

    def __init__(self):
        self.flag_final = True

    def parse_geo(self, url):
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
            df = gpd.read_file(url)
            #print("was fine")
            return df
        except:
            self.flag_final = False
            return gpd.GeoDataFrame()

    def load_data(self, url):
        """
        load data set for url

        PARAMETERS:
        -----------
        url: String
            Data ID based link

        RETURNS:
        -----------
        DataFrame: data for url
        Boolean: flag_final (success)
        """
        #print(self.flag_final)
        #print(result)
        return self.parse_geo(url), self.flag_final
