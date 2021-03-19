import os
import sys
import requests
import pandas as pd
import numpy as np
from colorama import init, Fore, Back, Style

init()  # colorama

from .config import Config as cf

from .fetch_dataset_list import DataSetUrlFetcher

from .fetcher.csv_fetcher import csvFetcher
from .fetcher.shp_fetcher import shpFetcher  # applies for some jsons as well
from .fetcher.xls_fetcher import xlsFetcher
from .fetcher.txt_fetcher import txtFetcher
from .fetcher.json_fetcher import jsonFetcher
from .fetcher.kml_fetcher import kmlFetcher

formats_dict = {
    "csv": csvFetcher,
    "txt": txtFetcher,
    "xls": xlsFetcher,
    "xlsx": xlsFetcher,
    "zip": shpFetcher,
    "geojson": shpFetcher,
    "json": jsonFetcher,
    "kml": kmlFetcher
}

dsuf = DataSetUrlFetcher()

# current_list = read_curr_packages()


class FetchHelper:
    """
    helper class containing functions for fetching
    """
    def __init__(self):
        pass

    def get_instance(format):
        """
        gets instance of repective fetcher

        PARAMETERS:
        -----------
        format: String
            file format (e.g. csv, json, ...)

        RETURNS:
        -----------
        Fetcher: respective fetcher
        """
        return formats_dict[format]

    def fetch_dataset_urls(id):
        """
        get urls corresponding to id

        PARAMETERS:
        -----------
        id: String
            package id

        RETURNS:
        -----------
        yield: url, name, format
        if staus code not 200
            return status code
        """
        response = requests.get(cf.PACKAGE_BASE_URL + id)
        if response.status_code == 200:
            resources = response.json()["result"][0]["resources"]
            for resource in resources:
                yield resource["url"], resource["format"], resource["name"]
        return response.status_code

    def get_url_ending(url):
        """
        get ending of url/file

        PARAMETERS:
        -----------
        url: String
            respective url

        RETURNS:
        -----------
        String: file type/url ending
        """
        if url[-4:] == "json" and url[-5:] != ".json":
            return "geojson"
        else:
            return url.split(".")[::-1][0].lower()

    def verify_url(self, url):
        """
        check if an url belongs to offenedaten-konstanz.de

        PARAMETERS:
        -----------
        id: String
            respective url

        RETURNS:
        -----------
        Boolean: if url has offene-daten as domain
        """
        return "offenedaten-konstanz.de" in url.lower()


class IdHelper:
    """
    helper class for creating id list
    """
    def __init__(self):
        self.current_list = dsuf.read_curr_packages()

    def create_id_list(data, tag=False):
        """
        helper function to create a list of ids for the datasets
        indicated by the names/tags given

        PARAMETERS:
        -----------
        data: list of Strings
            containing names or tags (string)
        tag: Boolean
            default: False
            set to True if data list contains tags

        RETURNS:
        -----------
        List<String>: list of ids
        """
        id_list = []
        if tag:
            for i in range(len(data)):
                for j in range(len(current_list)):
                    if data[i] in current_list.loc[j, "tags"]:
                        id_list.append(current_list.loc[j, "id"])
        else:
            for i in range(len(data)):
                if data[i] in current_list["name"].values:
                    id_element = np.array2string(current_list[
                        current_list['name'] == data[i]]['id'].values)
                    id_list.append(id_element[2:-2])
        return id_list
