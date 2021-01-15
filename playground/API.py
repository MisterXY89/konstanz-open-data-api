
import urllib.request
import os

from API_helper import *

current_list = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)
formats = ["csv","json","shp","xls","txt"]

def get_data(data, tag = False, external = False):
    """
    input : list containing names or tags (string)
    return : single df or dict containing df
    """
    id_list = IdHelper.create_id_list(data, tag)

    result_dict = {}
    #final_flag = True

    if external:
        print("These are external data sets. Please refer to ...")
    else:
        for i in range(len(id_list)):
            for url, format, name in FetchHelper.fetch_dataset_urls(id_list[i]):
                ending = FetchHelper.get_url_ending(url) # works also with Kn Gis Hub?
                if ending in formats:
                    instance = FetchHelper.get_instance(ending)()
                    df, flag = instance.load_data(url)
                else:
                    df = {}
                    flag = False
                key = name + " " + format
                result_dict[key] = df
                if flag:
                    print("Successfully loaded data set: " + key)
                else:
                    print("Data set was omitted: " + key)

                #if not flag:
                #    final_flag = False

        #if not final_flag:
        #print("Oopsie, something went wrong")

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

    id_list = IdHelper.create_id_list(data)

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


#test = get_data(["standorte_glascontainer"])
#test = get_data(["historische_wetterdaten"])
#test = get_data(["Geo"], tag=True)
#test = get_data(["Umwelt und Klima"], tag=True)
#save_data(["standorte_sportanlagen"], folder = "C:/Users/bikki/Downloads")
#save_data(["standorte_sportanlagen"])

