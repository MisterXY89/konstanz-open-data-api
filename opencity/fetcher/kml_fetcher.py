import json
import requests
from pandas import pandas as pd
import geopandas as gpd
import fiona

class kmlFetcher:
    """
    klmFetcher: fetches GeoData (KML)
    """

    def __init__(self):
        self.flag_final = True

    def enable_KML(self):
        """
        enable KML support
        """
        fiona.drvsupport.supported_drivers['kml'] = 'rw'
        fiona.drvsupport.supported_drivers['KML'] = 'rw'

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

        self.enable_KML()

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
