import os
import sys
import requests
import pandas as pd
import numpy as np
from tabulate import tabulate
import re
try:
    import tkinter as tk
    import tksheet
    TK = True
except Exception as e:
    TK = False

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
    
    def fetch_dataset_meta(id):
        """
        get meta data corresponding to id

        PARAMETERS:
        -----------
        id: String
            package id

        RETURNS:
        -----------
        yield: id, url, format, name, created, last_modified, description
        if staus code not 200
            return status code
        """
        response = requests.get(cf.PACKAGE_BASE_URL + id)
        if response.status_code == 200:
            resources = response.json()["result"][0]["resources"]
            for resource in resources:
                yield resource["id"], resource["url"], resource["format"], resource["name"], resource["created"], resource["last_modified"], resource["description"]
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
        if url[-5:] == "=json":
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
    def __init__(self, dsuf):
        self.dsuf = dsuf
        if hasattr(self.dsuf, "current_list"):
            self.current_list = self.dsuf.current_list
        else:
            self.current_list = read_curr_packages()

    def create_id_list(self, data, tag=False):
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
                for j in range(len(self.current_list)):
                    if data[i] in self.current_list.loc[j, "tags"]:
                        id_list.append(self.current_list.loc[j, "id"])
        else:
            for i in range(len(data)):
                if data[i] in self.current_list["name"].values:
                    id_element = np.array2string(self.current_list[
                        self.current_list['name'] == data[i]]['id'].values)
                    id_list.append(id_element[2:-2])
        if len(id_list) == 0:
            print("The provided names or tags are incorrect." + 
            "\nPlease check spelling. Note that the names for data sets are written in lower case, whereas tags are written with capital letters. " + 
            "\nAdditionally, make sure to set the parameter 'tag' to True if you specified a tag." + 
            "\nFurthermore, make sure to always provide the names of the data sets or tags as a list of strings.")
            spelling = False
        else:
            spelling = True
            
        return id_list, spelling

class ShowDataHelper: 
    """
    helper class for the show_data() function
    """

    def __init__(self, current_list):
        self.current_list = current_list

    def summary(self):
        tags = []
        for taglist in self.current_list.tags:
            clean = re.findall(r"\'(.*?)\'", taglist) #find everything enclosed by '...'
            for entry in clean: 
                if entry not in tags:
                    tags.append(entry)        
        print('There are in total {} datasets available.\nThese datasets belong to {} different categories.These categories are: {}'.format(len(self.current_list), len(tags), tags)) 
    
    def short(self, df):
        print(tabulate(df[['title', 'name', 'tags']], headers = ['Title', 'Shortname', 'Tags']))

    def long(self, df):
        long = pd.melt(df,id_vars = 'title')
        titles = long.title.unique()
        for element in titles: 
            df_element = long.loc[long['title'] == element]
            print(" \n" + element + " :\n" + tabulate(df_element[['variable', 'value']], headers = ['Variable', 'Value'], showindex=False))
    
    def meta(self, df):
        df = df[['title', 'name', 'id', 'modified', 'source', 'notes', 'tags']]
        df = df.values.tolist()
        headers = ['Title', 'Shortname', 'ID', 'Last edited on', 'Source', 'Notes', 'Tags']
        app = tk.Tk()
        table = tksheet.Sheet(app, height=1000, width = 2000)
        table.grid()
        table.headers(headers)
        table.enable_bindings(("single_select",
                       "row_select",
                       "column_width_resize",
                       "arrowkeys",
                       "right_click_popup_menu",
                       "copy"))
        table.change_theme(theme = "light blue")
        table.set_sheet_data(data = df, reset_highlights = True, reset_col_positions=True, reset_row_positions=True)
        table.set_all_cell_sizes_to_text(redraw = True)
        app.mainloop()
