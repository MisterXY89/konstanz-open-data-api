
import json
from tqdm import tqdm
import time
import requests

from config import *


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


	def _store(self, data):
		print(data["success"])
		if not "success" in data:
			print("json_invalid_error")
			return False

		try:
			with open(CURRENT_PACKAGE_LIST_FILE, "w", encoding='utf-8') as package_list_file:
				json.dump(data, package_list_file, ensure_ascii=False, indent=4)
			return True
		except Exception as writing_file_error:
			print("writing_file_error")
			return False


	def _parse_data(self, data):
		if not "success" in data:
			return False

		results = data["result"][0]
		out = {
			"unix_time" : time.time(),
			"success" : data["success"],
			"datasets" : []
		}
		for item in tqdm(results):
			out["datasets"].append({
				"id" : item["id"],
                "name" : item["name"], 
                "title" : item["title"],
                "state" : item["state"],
                "url" : "https://offenedaten-konstanz.de/api/3/action/package_show?id="+item["id"],
                "notes" : item["notes"]
			})
		return out


	def update(self):
		resp = self.fetch()
		if type(resp) == int:
			print(f"Error: status_code = {resp}")
			return False

		data = self._parse_data(resp)

		store_status = self._store(data)
		if not store_status:
			print("Error while storing json")
			return False

		return True
			

dsuf = DataSetUrlFetcher()
s = dsuf.update()