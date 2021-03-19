"""
Some basic constants & general config
"""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    CWD: str = os.getcwd()
    PKG_FOLDER: str = ""
    NAMES_FILE: str = "../names.csv"
    CURRENT_PACKAGE_LIST_FILENAME: str = "CURRENT_PACKAGE_LIST.csv"
    CURRENT_PACKAGE_LIST_FILE: str = f"{PKG_FOLDER}{CURRENT_PACKAGE_LIST_FILENAME}"
    PACKAGE_BASE_URL: str = "https://offenedaten-konstanz.de/api/3/action/package_show?id="
    CURRENT_PACKAGE_LIST_URL: str = "https://offenedaten-konstanz.de/api/3/action/current_package_list_with_resources"
