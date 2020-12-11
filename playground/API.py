import pandas as pd
import numpy as np
import requests
from config import *

from csv_fetcher import csvFetcher
#import shp_fetcher
#import xls_fetcher
#from txt_fetcher import txtFetcher

current_list = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)
#formats = ["csv", "xls", "txt", "shp"]
__formats = {
    #"txt": txtFetcher,
    "csv": csvFetcher
}

def __fetch_dataset_urls(id):
    response = requests.get(PACKAGE_BASE_URL + id)
    if response.status_code == 200:
        resources = response.json()["result"][0]["resources"]
        for resource in resources:
            yield resource["url"], resource["format"], resource["name"]
    return response.status_code

def __get_url_ending(url):
    return url.split(".")[::-1][0].lower()

def get_data(data, tag = False, external = False):
    """
    input : list containing names or tags (string)
    return : single df or dict containing df
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

    result_dict = {}
    final_flag = True
    for i in range(len(id_list)):
        for url, format, name in __fetch_dataset_urls(id_list[i]):
            ending = __get_url_ending(url) # works also with Kn Gis Hub?
            instance = __formats[ending]()
            df, flag = instance.load_data(url)
            if not flag:
                final_flag = False
            result_dict[name] = df

    if not final_flag:
        print("Oopsie, something went wrong")

    if len(result_dict) == 1:
        key = list(result_dict.keys())[0]
        result = result_dict[key]
    else:
        result = result_dict

    return result

#test = get_data(["Geo"], tag=True)
#test = get_data(["standorte_glascontainer"])
test = get_data(["historische_wetterdaten"])
print(test)