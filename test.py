
import os
import pandas as pd

from opencity import opencity as oc
from opencity import config as conf 

# ! run pytest interactive -> some test cases needs user input ! #

# -------------------- obj init prep -------------------- #

# change depending on test env
ABSOLUTE_DIR = "/home/dragonfly/Documents/CorrelAid/"

# change if file is renamed in future
PKG_FILENAME = "CURRENT_PACKAGE_LIST.csv"

# helper clean function to catch File does not exist errors
def clean(obj, file=True):
    try:
        if file: 
            os.remove(obj)
        else:
            os.removedirs(obj)
    except Exception as e:
        print(e)
    
# clean all files potentially laying arround
clean(PKG_FILENAME)
clean(f"existing_test_pkg_folder/{PKG_FILENAME}")
clean(f"test_pkg_folder/{PKG_FILENAME}")
clean("test_pkg_folder", file=False)
clean(f"{ABSOLUTE_DIR}{PKG_FILENAME}")

# -------------------- obj init -------------------- #

def test_obj_init_without_config():
    open_city = oc.OpenCity()
    assert isinstance(open_city, oc.OpenCity)

def test_obj_init_config():
    cf = conf.Config(PKG_FOLDER="")
    assert isinstance(cf, conf.Config)
    
def test_obj_init_with_config_relative_folder_non_existing():
    cf = conf.Config(PKG_FOLDER="test_pkg_folder/")
    open_city = oc.OpenCity(cf = cf)
    assert os.path.isfile(cf.CURRENT_PACKAGE_LIST_FILE)
    
def test_obj_init_with_config_relative_folder_non_existing_no_trailing_sep():
    cf = conf.Config(PKG_FOLDER="test_pkg_folder")
    open_city = oc.OpenCity(cf = cf)
    assert os.path.isfile(cf.CURRENT_PACKAGE_LIST_FILE)
    
def test_obj_init_with_config_relative_folder_existing():
    cf = conf.Config(PKG_FOLDER="existing_test_pkg_folder/")
    open_city = oc.OpenCity(cf = cf)
    assert os.path.isfile(cf.CURRENT_PACKAGE_LIST_FILE)

def test_obj_init_with_config_absolute_folder_existing():
    cf = conf.Config(PKG_FOLDER=ABSOLUTE_DIR)
    open_city = oc.OpenCity(cf = cf)
    assert os.path.isfile(cf.CURRENT_PACKAGE_LIST_FILE)
    
# -------------------- save_data -------------------- #
def test_save_data_no_target_one_source():
    open_city = oc.OpenCity()
    files = open_city.save_data(["parkplaetze"], file_ret=True)
    assert files    
    for file in files:
        assert os.path.isfile(file)
    # assert os.path.isfile("") # 
    
    
    # todo: alle data sets + kombis
    

    
