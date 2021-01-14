import pandas as pd
import numpy as np
import urllib.request
import os

from config import *
from fetch_helper import *

from csv_fetcher import csvFetcher
from shp_fetcher import shpFetcher # applies for json as well
from xls_fetcher import xlsFetcher
from txt_fetcher import txtFetcher

current_list = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)

def __create_id_list(data, tag = False):
    '''
    helper function to create a list of ids for the datasets indicated by the names/tags given
    '''
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

def get_data(data, tag = False, external = False):
    """
    input : list containing names or tags (string)
    return : single df or dict containing df
    """
    id_list = __create_id_list(data)

    result_dict = {}
    final_flag = True
    for i in range(len(id_list)):
        for url, format, name in FetchHelper.fetch_dataset_urls(id_list[i]):
            ending = FetchHelper.get_url_ending(url) # works also with Kn Gis Hub?
            instance = FetchHelper.get_instance(ending)()
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

def save_data(data, tag = False, folder=""): 
    '''
    function to save the indicated data (or data fitting the indicated tags) to your local disk
    
    INPUT:
    data: list of Strings 
        list containing names of the datasets you want to store 
        or tags for which you want to save the respective datasets
    tag: Boolean
        default: False
        set to True if data list contains tags
    folder: String
        default: empty
        if you wanted to save the data to a different folder than the one from which you are executing the python file,
        you could indicate the respective folder here (use either forward slashes '/' or double backward slashes '\\')
    '''
    #doesn't work for links leading to jsons 

    id_list = __create_id_list(data)

    # create list containing urls: (could possibly be made more compact if you used the __fetch_dataset_urls() function, but not sure how to use it)
    url_list = []
    for i in range(len(id_list)):
        for url, format, name in FetchHelper.fetch_dataset_urls(id_list[i]):
            url_list.append(url)

    # save all the files indicated by the urls: 
    for url in url_list: 
        file_name = ""
        if len(folder)>0: # if a specific folder was given:
            file_name = os.path.join(folder, url.rsplit('/', 1)[1])
        else: #if no local path is given: save to current working directory
            file_name = os.path.join(os.getcwd(), url.rsplit('/', 1)[1])
        urllib.request.urlretrieve (url, file_name) # command to actually save the data
        print("Finished saving requested data to " + file_name)

test = get_data(["Geo"], tag=True)
#test = get_data(["standorte_glascontainer"])
#test = get_data(["historische_wetterdaten"])
# print(test)
#save_data(["standorte_sportanlagen"], folder = "C:/Users/bikki/Downloads")
#save_data(["standorte_sportanlagen"])