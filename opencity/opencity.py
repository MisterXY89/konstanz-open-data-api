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
from .config import Config


class OpenCity:
    """
    docstring for OpenCity
    """

    # current_list = pd.read_csv(CURRENT_PACKAGE_LIST_FILE)
    def __init__(self, cf=None):
        self.formats = ["csv", "json", "zip", "xls", "txt", "geojson", "kml", "xlsx"]
        self.names_file = "" 
        self.current_packages_file = ""
        if not cf:
            cf = Config()
        self.cf = cf
        self.dsuf = DataSetUrlFetcher(cf)
        self.id_helper = IdHelper(self.dsuf)
        self.show_data_helper = ShowDataHelper(self.dsuf.current_list)


    def get_data(self, data=[], tag=False, meta=False):
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
                tqdm.write(f"{Fore.GREEN}[+]{Style.RESET_ALL} Successfully loaded meta data of {df_meta.shape[0]} data sets")

                    
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

                                key = (name + "_" + format).replace(" - ", "_").replace(" ", "_").lower()
                                result_dict[key] = df

                                tqdm.write(f"{Fore.GREEN}[+]{Style.RESET_ALL} Successfully loaded data set:\t {key}")


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
        file_return = []
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
                file_return.append(file_name)
            # if the url is the result of a get query for a geojson: 
            else:                
                geodf = shpFetcher()
                geodf.parse_geo(url).to_file(file_name, driver="GeoJSON")
                print("Finished saving requested data to " + file_name)
                file_return.append(file_name)
        return file_return


    def show_data(self, data = [], tag = False, overview = False, meta = False, terminal = False): 
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
            set to True if you wanted more detailed information on the datasets
            depending on paremeter 'terminal', whether you get the output in your console or as a popup
        data: list of Strings
            list containing names of the datasets you want to store
            or tags for which you want to save the respective datasets
        tag: Boolean
            default: False
            set to True if data list contains tags
        terminal: Boolean
            default: False
            set to True if you want to print the meta data in your console instead of a popup

        RETURNS:
        -----------
        void
        """

        #TODO: include check for whether the indicated names / tags are correct (already implemented in other functions?)

        if overview == True and meta == True or overview == False and meta == False and len(data) > 0 : 
            # print("You did not use the function correctly.\n" 
            # + "Use either the parameter 'overview' or the parameter 'meta'.\n" 
            # + "Use the parameter 'data' in addition if you only want to ....") #TODO adapt
            tqdm.write(f"{Fore.RED}You did not use the function correctly.")
            tqdm.write(f"{Fore.RED}Use either the parameter 'overview' OR the parameter 'meta'.")
            tqdm.write(f"{Fore.RED}Use the parameter 'data' in addition if you only want to get an overview or the metadata for specific datasets or tags.")
            tqdm.write(f"{Fore.RED}Set the parameter 'tag' to True if you indicated tags instead of single datasets under the 'data' parameter.{Style.RESET_ALL} ")

        # if no input is given: 
        elif overview == False and meta == False and len(data) == 0: 
            self.show_data_helper.summary()

        # if no dataset or tag is given: 
        elif len(data) == 0: 
            if overview == True: 
                self.show_data_helper.short(self.dsuf.current_list)
            if meta == True:
                self.show_data_helper.summary()
                if terminal: 
                    print("\nIn the following you will see detailed information on all the datasets:\n")
                    self.show_data_helper.long(self.dsuf.current_list)
                else: 
                    print("\nIn the following popup you will see detailed information on all the datasets:")
                    self.show_data_helper.meta(self.dsuf.current_list)

        # if a dataset or a tag is given: show only the indicated datasets
        elif len(data) > 0: 
            tag_df = pd.DataFrame(columns = ['title', 'name', 'tags'])
            if tag: #if a tag is given
                for element in data: 
                    tag_df = pd.concat([tag_df, self.dsuf.current_list[self.dsuf.current_list.tags.str.contains(element)]], axis = 0) # create df containing only the data sets with that tag
            else: #if a dataset is given
                for element in data: 
                    tag_df = pd.concat([tag_df, self.dsuf.current_list[self.dsuf.current_list.name.str.contains(element)]], axis = 0)
            tag_df = tag_df.drop_duplicates(subset = "title")
            if overview == True: 
                self.show_data_helper.short(tag_df)
            if meta == True:
                if terminal: 
                    print("In the following you will see detailed information on {}:".format(data))
                    self.show_data_helper.long(tag_df)
                else: 
                    print("In the following popup you will see detailed information on {}:".format(data))
                    self.show_data_helper.meta(tag_df)





            


#test = get_data(["standorte_glascontainer"])
#test = get_data(["historische_wetterdaten"])
#test = get_data(["Geo"], tag=True)
#test = get_data(["Umwelt und Klima"], tag=True)
#save_data(["standorte_sportanlagen"], folder = "C:/Users/bikki/Downloads")
#save_data(["standorte_sportanlagen"])
# test = get_data(["wahlbezirke"])

# TODO: check if really want to download (disable with param)
