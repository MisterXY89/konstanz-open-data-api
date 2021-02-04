import json
import requests
from config import *
from pandas import pandas as pd
import geopandas as gpd  # install
import fiona

class kmlFetcher:
    """
    KMLetcher: fetches GeoData (KML)
    """

    def __init__(self):
        self.flag_final = True

    def enable_KML(self):
        """enable KML support"""
        fiona.drvsupport.supported_drivers['kml'] = 'rw' 
        fiona.drvsupport.supported_drivers['KML'] = 'rw' 

    def parse_geo(self, url):
        """
        parses data from url to dataframe 

        INPUT:
        url: Data ID based link

        OUPUT: 
        data as a pandas GeoDataFrame object
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
        load data set 

        INPUT:
        url: Data ID based link

        OUPUT: 
        data as a pandas GeoDatFrame object
        flag_final
        """
        return self.parse_geo(url), self.flag_final