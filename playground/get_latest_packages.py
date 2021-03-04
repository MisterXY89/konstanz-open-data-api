
import os
import time

from fetch_dataset_list import DataSetUrlFetcher

dsuf = DataSetUrlFetcher()
CURRENT_PACKAGE_LIST_FILE = "CURRENT_PACKAGE_LIST.csv"
MAX_DAY_DELTA = 14

def check():
    modified_time = os.path.getmtime(CURRENT_PACKAGE_LIST_FILE)
    delta = time.time() - modified_time
    day_delta = delta/60/60/24
    # print(day_delta)
    if day_delta > MAX_DAY_DELTA:
        prompt = input("Your local list of available data packages is outdated. Do you want to download the latest version? [y/N]").lower()
        if prompt == "n":
            print("> Not downloading")
            return 0
        print("> Updating packages...")
        dsuf.update()



check()
