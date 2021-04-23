import os
import urllib.request
from tqdm import tqdm
from colorama import init, Fore, Back, Style
import re

init()

# for prod only!
import warnings
warnings.filterwarnings("ignore")

from .API_helper import *


class OpenCity:
    """
    docstring for OpenCity
    """

    # current_list = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)
    def __init__(self, cf):
        self.formats = ["csv", "json", "zip", "xls", "txt", "geojson", "kml", "xlsx"]
        self.names_file = "" 
        self.current_packages_file = ""
        self.cf = cf
        self.dsuf = DataSetUrlFetcher(cf)
        self.id_helper = IdHelper(self.dsuf)


    def get_data(self, data, tag=False, meta=False):
        """
        general get data function to be called by user

        PARAMETERS:
        -----------
        data: list of Strings
            containing names or tags (string)
        tag: Boolean
            default: False
            set to True if data list contains tags
        meta : Boolean
            default: False

        RETURNS:
        -----------
        DataFrame|dict: single df or dict containing df
        """
        # if not hasattr(self, 'id_list'):
        self.id_list, spelling = self.id_helper.create_id_list(data, tag)

        result_dict = {}
        #final_flag = True
        
        if spelling:

            if meta:
                print("Loading meta data")
                length = len(self.id_list)
                df_meta = pd.DataFrame(columns=['id', 'url', 'format', 'name', 'created', 'last_modified', 'description'])
                for i in range(length):#tqdm(range(length), total=length, desc=f"[#] "):
                    for id, url, format, name, created, last_modified, description in FetchHelper.fetch_dataset_meta(self.id_list[i]):
                        df_meta = df_meta.append({'id': id, 'url': url, 'format': format, 'name': name, 'created': created, 'last_modified': last_modified, 'description': description}, ignore_index=True)
                result_dict["meta"] = df_meta
                    
            else:
                print("Loading data")
                length = len(self.id_list)
                for i in tqdm(range(length), total=length, desc=f"[#] "):
                    for url, format, name in FetchHelper.fetch_dataset_urls(self.id_list[i]):
                        ending = FetchHelper.get_url_ending(url) # works also with Kn Gis Hub?
                        if ending in self.formats:
                            instance = FetchHelper.get_instance(ending)()
                            df, flag = instance.load_data(url)
                        #print(flag)

                            if flag:
                            # print("Successfully loaded data set: " + key)

                                key = name + "_" + format
                                result_dict[key] = df

                                tqdm.write(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Successfully loaded data set:\t {key}")


                            else:
                            # print("Data set was omitted: " + key)
                                output_name = name + "_" + format
                                tqdm.write(f"{Fore.RED}[x]{Style.RESET_ALL} Data set was omitted:\t\t {output_name}")
                        else:
     
                            tqdm.write(f"{Fore.YELLOW}[-]{Style.RESET_ALL} External Link:\t\t\t {name}\n\t\t\t\t\t Please visit {url}")


        if len(result_dict) == 1:
            key = list(result_dict.keys())[0]
            result = result_dict[key]
        else:
            result = result_dict

        return result


    def save_data(self, data, tag=False, folder=""):
        """
        function to save the indicated data (or data fitting the indicated tags)
        to your local disk

        PARAMETERS:
        -----------
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

        RETURNS:
        -----------
        void
        """
        #doesn't work for links leading to jsons

        # if not self.id_list:            
        self.id_list, spelling = self.id_helper.create_id_list(data, tag)

        url_list = []
        key_list = []
        for i in range(len(self.id_list)):
            for url, format, name in FetchHelper.fetch_dataset_urls(self.id_list[i]):
                ending = FetchHelper.get_url_ending(url) 
                if ending in self.formats:
                    url_list.append(url)
                    key_list.append(re.sub("[*:/<>?\|]", "-", name) + "." + ending) # removing special characters not appropriate for file names

        for url, key in zip(url_list, key_list):
            file_name = ""
            # if a specific folder was given:
            if len(folder)>0: 
                file_name = os.path.join(folder, key)
            # if no folder was given: save to current working directory
            else:
                file_name = os.path.join(os.getcwd(), key)
            # if the url leads to a file: 
            if url[-5:] != "=json":
                urllib.request.urlretrieve(url, file_name) 
                print("Finished saving requested data to " + file_name)
            # if the url is the result of a get query for a geojson: 
            else:                
                geodf = shpFetcher()
                geodf.parse_geo(url).to_file(file_name, driver="GeoJSON")
                print("Finished saving requested data to " + file_name)


    def show_data(overview = False, meta = False, tag = ""): 
        """
        function to get an overview of the data sets available

        PARAMETERS:
        -----------
        overview: Boolean
            default: False
            set to True if you wanted to get a short overview (title, short name, tags)
            of the datasets in your console
        meta: Boolean
            default: False
            set to True if you wanted more detailed information on the datasets in a table (popup)
        tag: String
            default: empty
            if you wanted to see the overview or the meta data only for datasets belonging
            to a specific tag, you could indicate the tag here

        RETURNS:
        -----------
        void
        """
        if overview == True and meta == True or overview == False and meta == False and len(tag) > 0: 
            print("You did not use the function correctly.\n" 
            + "Use either the parameter 'overview' or the parameter 'meta'.\n" 
            + "Use the parameter 'tag' in addition if needed.\n" 
            + "Default settings will be used now: \n")
            ShowDataHelper.summary()

        # if no input is given: 
        elif overview == False and meta == False and len(tag) == 0: 
            ShowDataHelper.summary()

        # if no tag is given: 
        elif len(tag) == 0: 
            if overview == True: 
                ShowDataHelper.short(current_list)
            if meta == True:
                ShowDataHelper.summary()
                print("\nIn the following you will see detailed information on all the datasets:")
                ShowDataHelper.meta(current_list)

        # if a tag is given: 
        elif len(tag) > 0: 
            tag_df = current_list[current_list.tags.str.contains(tag)] # create df containing only the data sets with that tag
            if overview == True: 
                ShowDataHelper.short(tag_df)
            if meta == True:
                print("In the following you will see detailed information on datasets with the tag {}:".format(tag))
                ShowDataHelper.meta(tag_df)


#test = get_data(["standorte_glascontainer"])
#test = get_data(["historische_wetterdaten"])
#test = get_data(["Geo"], tag=True)
#test = get_data(["Umwelt und Klima"], tag=True)
#save_data(["standorte_sportanlagen"], folder = "C:/Users/bikki/Downloads")
#save_data(["standorte_sportanlagen"])
# test = get_data(["wahlbezirke"])

# TODO: check if really want to download (disable with param)
