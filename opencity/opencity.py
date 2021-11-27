import os
import urllib.request
from tqdm import tqdm
from colorama import init, Fore, Back, Style
import re

# for handling geojson files, which cause an urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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
    def __init__(self, cf=None, interactive = True):
        self.formats = ["csv", "json", "zip", "xls", "txt", "geojson", "kml", "xlsx"]
        self.names_file = "" 
        self.current_packages_file = ""
        self._interactive=interactive
        if not cf:
            cf = Config()
        self.cf = cf
        self.dsuf = DataSetUrlFetcher(cf,interactive=self._interactive)
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
                for i in tqdm(range(length), total=length, desc=f"[Loading Progress] "):
                    number_files = len(requests.get(cf.PACKAGE_BASE_URL + self.id_list[i]).json()["result"][0]["resources"])
                    for id, url, format, name, created, last_modified, description in tqdm(FetchHelper.fetch_dataset_meta(self.id_list[i]), total = number_files, desc=f"[#] "):
                        df_meta = df_meta.append({'id': id, 'url': url, 'format': format, 'name': name, 'created': created, 'last_modified': last_modified, 'description': description}, ignore_index=True)
                result_dict["meta"] = df_meta
                tqdm.write(f"{Fore.GREEN}[+]{Style.RESET_ALL} Successfully loaded meta data of {df_meta.shape[0]} data sets")

                    
            else:
                print("Loading data")
                length = len(self.id_list)
                for i in tqdm(range(length), total=length, desc=f"[#] "):
                    number_files = len(requests.get(cf.PACKAGE_BASE_URL + self.id_list[i]).json()["result"][0]["resources"])
                    for url, format, name in tqdm(FetchHelper.fetch_dataset_urls(self.id_list[i]), total=number_files, desc=f"[Loading Progress] "):
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


    def save_data(self, data, tag=False, folder="", suppress=False, file_ret=False):
        """
        function to save the indicated data (or data fitting the indicated tags)
        to your local disk

        PARAMETERS:
        -----------
        data: list of Strings
            list containing names of the data sets you want to store
            or tags for which you want to save the respective data sets
        tag: Boolean
            default: False
            set to True if data list contains tags
        folder: String
            default: empty
            if you wanted to save the data to a different folder than the one from which you are executing the python file,
            you could indicate the respective folder here (use either forward slashes '/' or double backward slashes '\\')
        suppress: Boolean
            default: False
            set to True if you want to suppress the initial question asking whether you really want to download
        file_ret: Boolean
            default: False
            for testing purposes

        RETURNS:
        -----------
        void
        """
        self.id_list, spelling = self.id_helper.create_id_list(data, tag)

        url_list = []
        key_list = []
        file_return = []
        if spelling: 
            ## define folder:
            if len(folder)>0: 
                #if the indicated directory doesn't exist:
                if os.path.isdir(folder)==False and self._interactive: 
                    print(f"{Fore.RED}There is no folder with the name {folder}.{Style.RESET_ALL}")
                    inp = input("Do you wish to proceed (and let it be created)? [y/N]\n> ")
                    
                    if inp == "N":
                        print(f"{Fore.RED}> EXITING{Style.RESET_ALL}")
                        return
                    elif inp == "y":
                            os.mkdir(path = folder)   
                            print(f"{Fore.GREEN}> DIRECTORY CREATED{Style.RESET_ALL}")              
            else:
                folder = os.getcwd()
            
            ## check if user really wants to download:
            if suppress==False and self._interactive: 
                inp = input("Do you wish to download all the files belonging to " + ', '.join(data) + " and save them at '" + folder + "'? [y/N]\n> ")
                if inp == "N":
                    print(f"{Fore.RED}> ABORTING DOWNLOAD{Style.RESET_ALL}")
                    return 
                elif inp == "y":
                    print(f"{Fore.GREEN}> STARTING DOWNLOAD{Style.RESET_ALL}")

            for i in range(len(self.id_list)):
                for url, format, name in FetchHelper.fetch_dataset_urls(self.id_list[i]):
                    ending = FetchHelper.get_url_ending(url) 
                    if ending in self.formats:
                        url_list.append(url)
                        key_list.append(re.sub("[*:/<>?\|]", "-", name) + "." + ending) # removing special characters not appropriate for file names

            for url, key in tqdm(zip(url_list, key_list), total = len(url_list), desc=f"[Saving Progress] "):
                file_name = os.path.join(folder, key)
                try:
                    if url[-5:] != "=json":
                        urllib.request.urlretrieve(url, file_name) 
                        file_return.append(file_name)
                # if the url is the result of a get query for a geojson: 
                    else:                
                        geodf = shpFetcher()
                        geodf.parse_geo(url).to_file(file_name, driver="GeoJSON")
                        file_return.append(file_name)
                except: 
                    tqdm.write(f"{Fore.RED}[x]{Style.RESET_ALL} The file '{key}' could not be saved to your local disk. Please check its url: {url} {Style.RESET_ALL}")
        tqdm.write(f"{Fore.GREEN}[+]{Style.RESET_ALL} Finished saving requested data to '{folder}'.")
        
        # if file_ret:
        #    return file_return
        #return ""


    def show_data(self, data = [], tag = False, overview = False, meta = False, terminal = False): 
        """
        function to get an overview of the data sets available

        PARAMETERS:
        -----------
        overview: Boolean
            default: False
            set to True if you wanted to get a short overview (title, short name, tags)
            of the data sets in your console
        meta: Boolean
            default: False
            set to True if you wanted more detailed information on the data sets
            depending on paremeter 'terminal', whether you get the output in your console or as a popup
        data: list of Strings
            list containing names of the data sets you want to store
            or tags for which you want to save the respective data sets
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

        if overview == True and meta == True or overview == False and meta == False and len(data) > 0 or isinstance(tag, list): 
            tqdm.write(f"{Fore.RED}You did not use the function correctly.")
            tqdm.write(f"{Fore.RED}Use either the parameter 'overview' OR the parameter 'meta'.")
            tqdm.write(f"{Fore.RED}Use the parameter 'data' in addition if you only want to get an overview or the metadata for specific data sets or tags.")
            tqdm.write(f"{Fore.RED}Set the parameter 'tag' to True if you indicated tags instead of single data sets under the 'data' parameter.{Style.RESET_ALL} ")

        # if no input is given: 
        elif overview == False and meta == False and len(data) == 0: 
            self.show_data_helper.summary()

        # if no data set or tag is given: 
        elif len(data) == 0: 
            if overview == True: 
                self.show_data_helper.short(self.dsuf.current_list)
            if meta == True:
                self.show_data_helper.summary()
                if terminal: 
                    print("\nIn the following you will see detailed information on all the data sets:\n")
                    self.show_data_helper.long(self.dsuf.current_list)
                else:
                    if TK:             
                        print("\nIn the following popup you will see detailed information on all the data sets:")
                        self.show_data_helper.meta(self.dsuf.current_list)
                    else:
                        print(f"{Fore.RED}There is an error with your Tkinter installation, use terminal=True to show the information anyway.{Style.RESET_ALL}")

        # if a data set or a tag is given: show only the indicated data sets
        elif len(data) > 0: 
            #check spelling first:
            self.id_list, spelling = self.id_helper.create_id_list(data, tag)
            if spelling: 
                tag_df = pd.DataFrame(columns = ['title', 'name', 'tags'])
                if tag: #if a tag is given
                    for element in data: 
                        tag_df = pd.concat([tag_df, self.dsuf.current_list[self.dsuf.current_list.tags.str.contains(element)]], axis = 0) # create df containing only the data sets with that tag
                else: #if a data set is given
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
                        if TK:                            
                            print("In the following popup you will see detailed information on {}:".format(data))
                            self.show_data_helper.meta(tag_df)
                        else:
                            print(f"{Fore.RED}There is an error with your Tkinter installation, use terminal=True to show the information anyway.{Style.RESET_ALL}")
        
        else: 
            tqdm.write(f"{Fore.RED}You did not use the function correctly.")
            tqdm.write(f"{Fore.RED}Use either the parameter 'overview' OR the parameter 'meta'.")
            tqdm.write(f"{Fore.RED}Use the parameter 'data' in addition if you only want to get an overview or the metadata for specific data sets or tags.")
            tqdm.write(f"{Fore.RED}Set the parameter 'tag' to True if you indicated tags instead of single data sets under the 'data' parameter.{Style.RESET_ALL} ")