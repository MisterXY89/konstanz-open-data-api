"""
Some basic constants & general config
"""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    CWD: str = os.getcwd()
    PKG_FOLDER: str = ""
    NAMES_FILE: str = f"{PKG_FOLDER}names.csv" # todo create if not exiting
    CURRENT_PACKAGE_LIST_FILENAME: str = "CURRENT_PACKAGE_LIST.csv"
    NAMES_FILENAME: str = "names.csv"
    PACKAGE_BASE_URL: str = "https://offenedaten-konstanz.de/api/3/action/package_show?id="
    CURRENT_PACKAGE_LIST_URL: str = "https://offenedaten-konstanz.de/api/3/action/current_package_list_with_resources"
    GH_NAMES_FILE_URL: str = "https://raw.githubusercontent.com/MisterXY89/konstanz-open-data-api/master/names.csv"
    PATH_SEP: str = os.sep
    
    CURRENT_PACKAGE_LIST_FILE: str = field(init=False)
    NAMES_FILE: str = field(init=False)

    def __post_init__(self):
        sep = ""
        if self.PKG_FOLDER != "":            
            if self.PKG_FOLDER[-1] != self.PATH_SEP:
                sep = self.PATH_SEP
            if not self.PKG_FOLDER[0] == "C" or not self.PKG_FOLDER[0] == "/": # relative path
                if not os.path.isdir(self.PKG_FOLDER):
                    os.mkdir(self.PKG_FOLDER)
                
        self.CURRENT_PACKAGE_LIST_FILE: str = f"{self.PKG_FOLDER}{sep}{self.CURRENT_PACKAGE_LIST_FILENAME}" # /????
        self.NAMES_FILE: str = f"{self.PKG_FOLDER}{sep}{self.NAMES_FILENAME}"    