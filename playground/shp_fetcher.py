import json
import requests
from config import *
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

        INPUT:
        url: Data ID based link

        OUPUT: 
        data as a pandas GeoDatFrame object
        """
        try: 
            df = gpd.read_file(url)
            return df
        except: 
            self.flag_final = False
            return gpd.GeoDataFrame()

    def load_data(self, url):
        """
        load data set 

        INPUT:
        url: Data ID based link

        OUPUT: 
        data as a pandas GeoDatFrame object
        flag_final
        """
        return self.parse_geo(url), self.flag_final