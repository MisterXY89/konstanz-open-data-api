
import time
import os
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import math

from config import CURRENT_PACKAGE_LIST_FILE


class DataSetUrlFetcher(object):
	"""
	docstring for DataSetFetcher
	"""
	def __init__(self):
		self.CURRENT_PACKAGE_LIST_URL = "https://offenedaten-konstanz.de/api/3/action/current_package_list_with_resources"
		# self.CURRENT_PACKAGE_LIST_FILE = "CURRENT_PACKAGE_LIST.json"
		# self.header = request_settings.header

	def fetch(self):
		response = requests.get(self.CURRENT_PACKAGE_LIST_URL) # , header =
		if response.status_code == 200:
			return response.json()
		return response.status_code


	def _store(self, data_frame:pd.DataFrame) -> bool:
		if not isinstance(data_frame, pd.DataFrame):
			print(f"Expected DataFrame, got {type(data_frame)}")
			return False

		try:
			parent_dir = os.path.join(os.getcwd(), '..', 'names.csv')
			name_list = pd.read_csv(parent_dir, sep=';')
			merged_list = pd.merge(data_frame, name_list, how='left', on='id')
			merged_list.to_csv(CURRENT_PACKAGE_LIST_FILE, encoding='utf-8', index=False)
			#print(merged_list)
			return True
		except Exception as writing_file_error:
			print(writing_file_error)
			return False


	def _parse_data(self, data):
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
					"id" : item["id"],
                	"title" : item["title"],
                	"source" : item["url"],
                	"url" : "https://offenedaten-konstanz.de/api/3/action/package_show?id="+item["id"],
					"created": item["metadata_created"],
					"modified": item["metadata_modified"],
                	"notes" : BeautifulSoup(item["notes"], "lxml").text,
					"tags" : tags
				})
			except:
				print("item has not all information needed") # concerns data set 'test' on OpenData website
		return pd.DataFrame.from_dict(out)


	def update(self):
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
