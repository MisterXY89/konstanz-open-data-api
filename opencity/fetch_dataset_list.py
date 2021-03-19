import os
import time
import math
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

init()  # colorama

from .config import Config as cf


class DataSetUrlFetcher(object):
    """
	Handles the fetching and storing of all available datasets
	"""
    def __init__(self):
        self.current_list = self.read_curr_packages()

    def read_curr_packages(self):
        try:
            result = pd.read_csv(cf.CURRENT_PACKAGE_LIST_FILE)
        except Exception as e:
            print(
                f"{Fore.RED}There is no file with name {cf.CURRENT_PACKAGE_LIST_FILENAME} in the current directory: {cf.CWD}.{Style.RESET_ALL}"
            )
            inp = input(
                "The file is needed, do you wish to proceed (and let it be created)? [y/N]"
            )
            if inp == "N":
                print(f"{Fore.RED}> EXITING")
                sys.exit(0)
                return 0
            resp = self.fetch()
            if isinstance(resp, int):
                print(f"Error: status_code = {resp}")
                return False

            data_frame = self._parse_data(resp)
            self._store(data_frame)
            return data_frame

    def fetch(self):
        """
		basic fetch method for the cf.CURRENT_PACKAGE_LIST_URL

		PARAMETERS:
		-----------
		None

		RETURNS:
		-----------
		Json: current packages (success)
		Int: Status code (error)
		"""
        response = requests.get(cf.CURRENT_PACKAGE_LIST_URL)  # , header =
        if response.status_code == 200:
            return response.json()
        return response.status_code

    def _store(self, data_frame: pd.DataFrame) -> bool:
        """
		writes dataframe to file

		PARAMETERS:
		-----------
		data_frame: DataFrame
			the respective DataFrame to store

		RETURNS:
		-----------
		sucess: Boolean
			indicates wether the storing was successfull
		"""
        if not isinstance(data_frame, pd.DataFrame):
            print(f"Expected DataFrame, got {type(data_frame)}")
            return False

        try:
            parent_dir = os.path.join(cf.CWD, '..', 'names.csv')
            name_list = pd.read_csv(parent_dir, sep=';')
            merged_list = pd.merge(data_frame, name_list, how='left', on='id')
            merged_list.to_csv(cf.CURRENT_PACKAGE_LIST_FILE,
                               encoding='utf-8',
                               index=False)
            #print(merged_list)
            return True
        except Exception as writing_file_error:
            print(writing_file_error)
            return False

    def _parse_data(self, data):
        """
		parse data from json into DataFrame

		PARAMETERS:
		-----------
		data: string (json)
			json string fetched for a resource

		RETURNS:
		-----------
			DataFrame with all info
		"""
        if not "success" in data:
            return False

        results = data["result"][0]

        out = list()
        for item in tqdm(results):
            tags = []
            try:
                for tag_item in item["tags"]:
                    tags.append(tag_item["name"])
                out.append({
                    "id":
                    item["id"],
                    "title":
                    item["title"],
                    "source":
                    item["url"],
                    "url":
                    "https://offenedaten-konstanz.de/api/3/action/package_show?id="
                    + item["id"],
                    "created":
                    item["metadata_created"],
                    "modified":
                    item["metadata_modified"],
                    "notes":
                    BeautifulSoup(item["notes"], "lxml").text,
                    "tags":
                    tags
                })
            except:
                print("item has not all information needed"
                      )  # concerns data set 'test' on OpenData website
        return pd.DataFrame.from_dict(out)

    def update(self):
        """
		update method which handles the fetching, parsing
		and storing of the info

		PARAMETERS:
		-----------
		None

		RETURNS:
		-----------
		success: Boolean
			wether the operation was successfull
		"""
        resp = self.fetch()
        if isinstance(resp, int):
            print(f"Error: status_code = {resp}")
            return False

        data_frame = self._parse_data(resp)
        # check if names are missing !!!!
        #print(data_frame)

        #store_status = self._store("st")
        store_status = self._store(data_frame)
        if not store_status:
            print("Error while storing data")
            return False

        return True


# dsuf = DataSetUrlFetcher()
# s = dsuf.update()
