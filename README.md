# Opencity

`Opencity` is an interface for the open data portal of Constance. This package allows you to directly inspect and download data and can be easily used by practioniers, members of the civil society and academics. Technically, it relies on the DKAN API.

## Capabilities
- get an overview of data sets via `show_data()`
- load data directly into Python via `get_data()`
- download data sets onto your local machine via `save_data()`

Generally, each functionality can be filtered by names and tags of the different data sets and returns pandas.DataFrames. It is easy to install, use, and work with.

#### _class_ `opencity.OpenCity`_(cf = None)_
> TODO

#### `OpenCity.show_data`_(data=[], tag=False, overview=False, meta=False, terminal=False)_
> displays an overview of the available and indicated data sets to the terminal or as a popup

> Parameters: 
> - **data: list of Strings, default: empty list** <br /> 
>   containing names or tags
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **overview: Boolean, default: False** <br /> 
>   set to True if a short overview of the data sets (title, short name, tags) is desired in the console
> - **meta: Boolean, default: False** <br /> 
>   set to True if more detailed information on the datasets is desired
>   depending on parameter 'terminal'
> - **terminal: Boolean, default: False** <br /> 
>   set to True if meta data should be printed in the console instead of a popup

> Returns: void
> 
#### `OpenCity.get_data`_(data=[], tag=False, meta=False)_
> retrieves the indicated data from the open data portal of Constance https://offenedaten-konstanz.de

> Parameters: 
> - **data: list of Strings, default: empty list** <br /> 
>   containing names or tags
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **meta : Boolean, default: False** <br /> 
>   set to True if meta data should be returned

> Returns: pandas.DataFrame | dict containing pandas.DataFrames

#### `OpenCity.save_data`_(data, tag=False, folder="")_
> saves the indicated data to the local disk

> Parameters: 
> - **data: list of Strings** <br /> 
>   containing names or tags
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **folder: String, default: empty** <br /> 
>   If you want to save the data to a different folder than the one from which you are executing the python file, indicate the respective folder here (use either forward slashes '/' or double backward slashes '\\')

> Returns: void

## Examples

### At first: Create an instance of the class OpenCity
```python
from opencity import config as conf
from opencity import opencity as oc
cf = conf.Config(PKG_FOLDER=path)
open_city = oc.OpenCity(cf=cf)
```
#### Show all available datasets
```python
open_city.show_data()
```
#### TODO: other functionalities of show_data() function

#### TODO: get_data() function examples

#### Save data of a dataset
```python
open_city.save_data(["solarpotenzial"]) #you could also indicate several datasets here
```
> The output will look something like this: <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Solarpotenzial 2018.csv` <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Solarpotenzial 2018.kml` <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Solarpotenzial 2018.zip` <br /> 
> `Finished saving requested data to C:\Users\username\Desktop\Solarpotenzial 2018.geojson` <br /> 

#### Save data of a tag
```python
open_city.save_data(["Geo"], tag = True) #you could also indicate several tags here
```
#### Save data to another folder than your project directory
```python
path = "C:/Users/example_path" #important to use either forward slashes or double backward slashes!
opencity.save_data(["standorte_sportanlagen"], folder = path)
```


## Installation

```bash
pip install opencity
```

### Potential problems
#### GeoPandas
....
#### something else
...



## Found a bug?
Open an issue including OS, package- and python version, executed code and error message!

## Author Information

Birke Pfeifle <br />
Rahkakavee Baskaran <br />
Tilman Kerl <br />
Silke Husse <br />

Email: konstanz@correlaid.org
