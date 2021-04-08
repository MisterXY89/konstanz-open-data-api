import os
import requests
import pandas as pd
import numpy as np
from tabulate import tabulate
import re
import tkinter as tk
import tksheet

from .config import (
        PKG_FOLDER,
        CURRENT_PACKAGE_LIST_FILE,
        PACKAGE_BASE_URL
        )

from .fetcher.csv_fetcher import csvFetcher
from .fetcher.shp_fetcher import shpFetcher # applies for some jsons as well
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

current_list = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)

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
        response = requests.get(PACKAGE_BASE_URL + id)
        if response.status_code == 200:
            resources = response.json()["result"][0]["resources"]
            for resource in resources:
                yield resource["url"], resource["format"], resource["name"]
        return response.status_code

    def get_url_ending(url):
        if url[-5:] == "=json":
            return "geojson"
        else:
            return url.split(".")[::-1][0].lower()

    def verify_url(self, url):
        """
        check if an url belongs to offenedaten-konstanz.de
        """
        return "offenedaten-konstanz.de" in url.lower()

class IdHelper:
    """
    helper class for creating id list
    """
    def __init__(self):
        pass

    def create_id_list(data, tag = False):
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
        """
        id_list = []
        if tag:
            for i in range(len(data)):
                for j in range(len(current_list)):
                    if data[i] in current_list.loc[j,"tags"]:
                        id_list.append(current_list.loc[j,"id"])
        else:
            for i in range(len(data)):
                if data[i] in current_list["name"].values:
                    id_element = np.array2string(current_list[current_list['name'] == data[i]]['id'].values)
                    id_list.append(id_element[2:-2])
        return id_list

class ShowDataHelper: 
    """
    helper class for the show_data() function
    """

    def __init__(self):
        pass

    def summary():
        tags = []
        for taglist in current_list.tags:
            clean = re.findall(r"\'(.*?)\'", taglist) #find everything enclosed by '...'
            for entry in clean: 
                if entry not in tags:
                    tags.append(entry)        
        print('There are in total {} datasets available.\nThese datasets belong to {} different categories.These categories are: {}'.format(len(current_list), len(tags), tags)) 
    
    def short(df):
        print(tabulate(df[['title', 'name', 'tags']], headers = ['Title', 'Token', 'Tags']))

    def meta(df): #TODO Output als HTML
        df = df[['title', 'name', 'id', 'modified', 'source', 'notes', 'tags']]
        df = df.values.tolist()
        headers = ['Title', 'Token', 'ID', 'Last edited on', 'Source', 'Notes', 'Tags']
        app = tk.Tk()
        table = tksheet.Sheet(app, height=1000, width = 2000)
        table.grid()
        table.headers(headers)
        table.set_sheet_data(data = df, reset_highlights = True, reset_col_positions=True, reset_row_positions=True)
        table.set_all_cell_sizes_to_text(redraw = True)
        app.mainloop()
