import json
import requests
from config import *
from pandas import pandas as pd
import geopandas as gpd  # install

class SHPFetcher:
    """
    """

    def __init__(self):
        self.seperator = ";"

    def fetch_dataset_urls(self, p_id):
        response = requests.get(PACKAGE_BASE_URL + p_id)  # , header=
        if response.status_code == 200:
            return response.json()["result"][0]["resources"][0]["url"]
        return response.status_code

    def verify_url(self, url):
        """
        check if an url belongs to offene-daten-konstanz.de
        """
        return "offenedaten-konstanz.de" in url

    def get_file_ending(self, url):
        """
        extract file ending from an url
        """
        return url.split(".")[::-1][0]

    def load_data(self, p_id):
        print(f"Loading data for {p_id}")
        url = self.fetch_dataset_urls(p_id)
        if self.verify_url(url) and self.get_file_ending(url) == "zip":
            data = gpd.read_file(url)
            return data

#
#import matplotlib.pyplot as plt
# tink_id = "c6ed879e-9a2c-41ca-a168-a88d449a24c1"
# dsf = SHPFetcher()
# data = dsf.load_data(tink_id)
# data.plot()
# plt.show()