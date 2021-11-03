import os
import time

from .config import Config as cf
from .fetch_dataset_list import DataSetUrlFetcher

dsuf = DataSetUrlFetcher()

MAX_DAY_DELTA = 14

def check():
    """
    check if local version of the current packages is up to date:
    if it has not been modified/updated in the last 14 days then ask user if he wants to update
    """
    if not dsuf.current_list:
        dsuf.update()
        return 1
    modified_time = os.path.getmtime(cf.CURRENT_PACKAGE_LIST_FILE)
    delta = time.time() - modified_time
    day_delta = delta / 60 / 60 / 24

    if day_delta > MAX_DAY_DELTA:
        prompt = input(
            "Your local list of available data packages is outdated. Do you want to download the latest version? [y/N]"
        ).lower()
        if prompt == "n":
            print("> Not downloading")
            return 0
        print("> Updating packages...")
        dsuf.update()
