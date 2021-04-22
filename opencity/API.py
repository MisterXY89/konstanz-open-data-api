import os
import urllib.request
from tqdm import tqdm
from colorama import init, Fore, Back, Style

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


    def get_data(self, data, tag=False, external=False):
        """
        general get data function to be called by user

        PARAMETERS:
        -----------
        data: list of Strings
            containing names or tags (string)
        tag: Boolean
            default: False
            set to True if data list contains tags
        external: Boolean
            default: False
            TODO: set to True if data list contains external links

        RETURNS:
        -----------
        DataFrame|dict: single df or dict containing df
        """
        # if not hasattr(self, 'id_list'):
        self.id_list = self.id_helper.create_id_list(data, tag)

        result_dict = {}
        #final_flag = True

        if external:
            print("These are external data sets. Please refer to ...")
        else:
            print("Loading data")
            length = len(self.id_list)
            for i in tqdm(range(length), total=length, desc=f"[#] "):
                for url, format, name in FetchHelper.fetch_dataset_urls(
                        self.id_list[i]):
                    ending = FetchHelper.get_url_ending(
                        url)  # works also with Kn Gis Hub?
                    if ending in self.formats:
                        instance = FetchHelper.get_instance(ending)()
                        df, flag = instance.load_data(url)
                        #print(flag)

                        if flag:
                            # print("Successfully loaded data set: " + key)

                            key = name + " " + format
                            result_dict[key] = df

                            tqdm.write(
                                f"{Fore.GREEN}[✓]{Style.RESET_ALL} Successfully loaded data set:\t {key}"
                            )

                        else:
                            # print("Data set was omitted: " + key)
                            output_name = name + " " + format
                            tqdm.write(
                                f"{Fore.RED}[x]{Style.RESET_ALL} Data set was omitted:\t\t {output_name}"
                            )
                    else:
                        #df = {}
                        #flag_external = True
                        tqdm.write(
                            f"{Fore.YELLOW}[-]{Style.RESET_ALL} External Link:\t\t\t {name}\n\t\t\t\t\t Please visit {url}"
                        )

                    #if flag_external:

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
        self.id_list = self.id_helper.create_id_list(data, tag)

        url_list = []
        for i in range(len(self.id_list)):
            for url, format, name in FetchHelper.fetch_dataset_urls(self.id_list[i]):
                url_list.append(url)

        # save all the files indicated by the urls:
        for url in url_list:
            file_name = ""
            if len(folder) > 0:  # if a specific folder was given:
                file_name = os.path.join(folder, url.rsplit('/', 1)[1])
            else:  #if no local path is given: save to current working directory
                file_name = os.path.join(os.getcwd(), url.rsplit('/', 1)[1])
            urllib.request.urlretrieve(
                url, file_name)  # command to actually save the data
            print("Finished saving requested data to " + file_name)


#test = get_data(["standorte_glascontainer"])
#test = get_data(["historische_wetterdaten"])
#test = get_data(["Geo"], tag=True)
#test = get_data(["Umwelt und Klima"], tag=True)
#save_data(["standorte_sportanlagen"], folder = "C:/Users/bikki/Downloads")
#save_data(["standorte_sportanlagen"])
# test = get_data(["wahlbezirke"])

# TODO: check if really want to download (disable with param)