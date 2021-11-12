opencity
================

<img src='logo_package.png' align="right" height="139" />

<!-- badges: start -->
[![Project Status: Active – The project has reached a stable, usable
state and is being actively
developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![PyPI version shields.io](https://img.shields.io/pypi/v/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
<!-- badges: end -->

`opencity` is an interface for the [open data portal of Constance](https://offenedaten-konstanz.de). It allows you to directly inspect, download, and work with the available data. This package can be easily used by practitioners, members of the civil society, and academics. Technically, it relies on the DKAN API. <br>
Install using pip. For potential problems see the the [Installation and Problems part](#install).
```bash
pip install opencity
```

- [Installation](#install)
  - [Potential problems](#install_prob)
- [Capabilities](#capabilities)
  - [Class OpenCity](#class) 
    - [Properties](#properties)
    - [Functions](#functions)
      - [show_data](#show)
      - [get_data](#get)
      - [save_data](#save)
- [Examples](#examples)
  - [show_data](#ex_show)
  - [get_data](#ex_get)
  - [save_data](#ex_save)
- [Author information](#authors) 


<a name="install"></a>
## Installation
```bash
pip install opencity
```

<a name="install_prob"></a>
### Potential problems
#### GeoPandas
When installing the opencity package on a *Windows* computer, you might run into trouble during the installation due to the package requirement `geopandas`.
This package is necessary for reading in spatial data, which is available for some of the data sets. 
Please try [this towardsdatascience article](https://towardsdatascience.com/geopandas-installation-the-easy-way-for-windows-31a666b3610f) for assistance in installing `geopandas` and then try to install opencity again.

#### tk / tkinter
The show_data method has one option to show meta data of available data-sets in a popup window. 
If you want to use this feature and run into errors (e.g. *There is an error with your Tkinter installation, use terminal=True to show the information anyway* )
see [this AskUbuntu Question](https://askubuntu.com/questions/1224230/how-to-install-tkinter-for-python-3-8#1236924) or [this StackOverflow Question](https://askubuntu.com/questions/1224230/how-to-install-tkinter-for-python-3-8#1236924).

However, you can always use the `terminal=True` parameter to display the same information in the terminal.

#### SSL: CERTIFICATE_VERIFY_FAILED
For later versions of Python on *macOS*, certificates are not pre-installed which seems to cause this error:

```urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)```

See [this StackOverflow Question](https://stackoverflow.com/a/57941428) for a solution.

<a name="capabilities"></a>
## Capabilities
- get an overview of data sets via [`show_data()`](#show)
- load data directly into Python via [`get_data()`](#get)
- download data sets onto your local machine via [`save_data()`](#save)

Generally, each functionality can be filtered by names and tags of the different data sets.

<a name="class"></a>
### _class_ `opencity.OpenCity`_(cf = None)_
class with several features described in the following

<a name="properties"></a>
#### Properties :
> - **formats** <br />
>   list of Strings specifying formats
> - **cf** <br />
>   reference to configuration file containing all relevant information
> - **(various) helper classes** <br />
>   reference to various files containing helper classes

<a name="functions"></a>
#### Functions :
> - **show_data()** <br />
> - **get_data()** <br />
> - **save_data()** <br />

Each functionality is described in the following in detail.

<a name="show"></a>
#### `OpenCity.show_data`_(data=[], tag=False, overview=False, meta=False, terminal=False)_
displays an overview of the available and indicated data sets to the terminal or as a popup

> Parameters: 
> - **data: list of Strings, default: empty list** <br /> 
>   containing names or tags
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **overview: Boolean, default: False** <br /> 
>   set to True if a short overview of the data sets (title, short name, tags) is desired in the console
> - **meta: Boolean, default: False** <br /> 
>   set to True if more detailed information on the data sets is desired
>   depending on parameter 'terminal'
> - **terminal: Boolean, default: False** <br /> 
>   set to True if meta data should be printed in the console instead of a popup

> Returns: void

<a name="get"></a>
#### `OpenCity.get_data`_(data=[], tag=False, meta=False)_
retrieves the indicated data from the [open data portal of Constance](https://offenedaten-konstanz.de)

> Parameters: 
> - **data: list of Strings, default: empty list** <br /> 
>   containing names or tags
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **meta : Boolean, default: False** <br /> 
>   set to True if meta data should be returned

> Returns: `pandas.DataFrame` | dict containing `pandas.DataFrame`s

<a name="save"></a>
#### `OpenCity.save_data`_(data, tag=False, folder="")_
saves the indicated data to the local disk

> Parameters: 
> - **data: list of Strings** <br /> 
>   containing names or tags
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **folder: String, default: empty** <br /> 
>   If you want to save the data to a different folder than the one from which you are executing the python file, indicate the respective folder here (use either forward slashes '/' or double backward slashes '\\')

> Returns: void

<a name="examples"></a>
## Examples

In the following, we use `<shortname>` as a placeholder for the actual shortnames of each data set. To find out about the actual shortnames, you can use `open_city.show_data(overview = True)` and check the second column.

As a placeholder for the actual tags we use `<Tag>`. To find out about all the available tags, you can use `open_city.show_data()`.

### At first: create an instance of the class OpenCity
```python
from opencity import opencity as oc
from opencity import config as conf

path = "<path>" # specify path here
cf = conf.Config(PKG_FOLDER=path)
open_city = oc.OpenCity(cf=cf)
```
Alternatively you can init an OpenCity object without specifying a path - the file holding all current datasets will then be stored in the current working directory:
```python
from opencity import opencity as oc
open_city = oc.OpenCity()
```
<a name="ex_show"></a>
### show_data()

#### show the total number of available data sets and their tags
```python
open_city.show_data()
```
#### show an overview 
```python
# of all available data sets:
open_city.show_data(overview = True)

# of all indicated data sets:
open_city.show_data(overview = True, data = ["<shortname>"]) #indicate one or several data sets as a list of Strings, using their shortname

# of all available data sets belonging to a certain tag:
open_city.show_data(overview = True, data = ["<Tag>"], tag = True) #indicate one or several tags as a list of Strings
```
#### show meta data in a popup table
```python
# of all available data sets: 
open_city.show_data(meta = True)

# of all indicated data sets:
open_city.show_data(meta = True, data = ["<shortname>"]) #indicate one or several data sets as a list of Strings, using their shortname

# of all available data sets belonging to a certain tag:
open_city.show_data(meta = True, data = ["<Tag>"], tag = True) #you could also indicate several tags here
```
#### show meta data in the terminal
```python
open_city.show_data(meta = True, terminal = True) #indicate one or several tags as a list of Strings
```
<a name="ex_get"></a>
### get_data()

#### get data of a data set
```python
open_city.get_data(data = ["<shortname>"]) #indicate one or several data sets as a list of Strings, using their shortname
```
> The output will look something like this: <br /> 
> `Loading data` <br />
> `[+] Successfully loaded data set:        radverkehr_kampagne_stadtradeln_konstanz_2018_csv` <br />
> `[+] Successfully loaded data set:        radverkehr_kampagne_stadtradeln_konstanz_2019_csv` <br />
> `[+] Successfully loaded data set:        radverkehr_kampagne_stadtradeln_konstanz_2020_csv` <br />

#### get data of a tag
```python
open_city.get_data(data = ["<Tag>"], tag = True) #indicate one or several tags as a list of Strings
```
> The output will look something like this: <br /> 
> `Loading data` <br />
> `[+] Successfully loaded data set:        einträge_im_mängelmelder_2017_csv` <br />
> `[-] External Link:                       Einträge im Mängelmelder 2017                                                  
					 Please visit https://konstanz.hub.arcgis.com/datasets/Konstanz::eintr%C3%A4ge-im-m%C3%A4ngelmelder-seit-dem-01-01-17` <br />
> `[+] Successfully loaded data set:        außenwanderung_bei_stadtteil_von_2011_bis_2019_csv` <br />
> `[+] Successfully loaded data set:        kindertagesbetreuung_einrichtungen_csv` <br />
> `[+] Successfully loaded data set:        kindertagesbetreuung_einrichtungen_json` <br />

#### get meta data of a data set
```python
open_city.get_data(data = ["<shortname>"], meta = True) #indicate one or several data sets as a list of Strings, using their shortname
```
> The output will look something like this: <br /> 
> `Loading data` <br />
> `[+] Successfully loaded meta data of 6 data sets` <br />

#### get meta data of a tag
```python
open_city.get_data(data = ["<Tag>"], tag = True, meta = True) #indicate one or several tags as a list of Strings
```
> The output will look something like this: <br /> 
> `Loading data` <br />
> `[+] Successfully loaded meta data of 16 data sets` <br />

<a name="ex_save"></a>
### save_data()

#### save data of a data set
```python
open_city.save_data(data = ["<shortname>"]) #indicate one or several data sets as a list of Strings, using their shortname
```
> The output will look something like this: <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Standorte Sportanlagen.csv`  <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Standorte Sportanlagen.zip`  <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Standorte Sportanlagen.geojson`   <br /> 

#### save data of a tag
```python
open_city.save_data(data = ["<Tag>"], tag = True) #indicate one or several tags as a list of Strings
```
#### save data to another folder than your project directory
```python
path = "C:/Users/example_path" #important to use either forward slashes or double backward slashes!
open_city.save_data(data = ["<shortname>"], folder = path)
```



## Found a bug?
Open an issue including OS, package- and python version, executed code and error message!

<a name="authors"></a>
## Author Information

Birke Pfeifle <br />
Rahkakavee Baskaran <br />
Tilman Kerl <br />
Silke Husse <br />

Email: konstanz@correlaid.org
