# Opencity

`Opencity` is an interface for the open data portal of the city of Constance.

## Capabilities
- Search by tags, name and ID
- Returns pandas DataFrame
- easy install and workflow

#### _class_ `opencity.OpenCity`_(cf = None)_
> TODO

#### `OpenCity.get_data`_(data, tag=False, meta=False)_
> Retrieves data from OpenData.

> Parameters: 
> - **data: list of Strings** <br /> 
>   containing names or tags (string)
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **meta : Boolean, default: False** <br /> 

> Returns: DataFrame|dict: single df or dict containing df

#### `OpenCity.save_data`_(data, tag=False, folder="")_

> Saves the indicated data (or data fitting the indicated tags) to the local disk.

> Parameters: 
> - **data: list of Strings** <br /> 
>   A list containing names of the datasets you want to store or tags for which you want to save the respective datasets.
> - **tag: Boolean, default: False** <br /> 
>   Set this parameter to True if the *data* list contains tags.
> - **folder: String, default: empty** <br /> 
>   If you wanted to save the data to a different folder than the one from which you are executing the python file, you could indicate the respective folder here (use either forward slashes '/' or double backward slashes '\\').

> Returns: void

#### `OpenCity.show_data`_(overview = False, meta = False, data = [], tag = False, terminal = False)_
> Returns an overview of the data sets available to the terminal or as a popup.

> Parameters: 
> - **overview: Boolean, default: False** <br /> 
>   set to True if you wanted to get a short overview (title, short name, tags) of the datasets in your console
> - **meta: Boolean, default: False** <br /> 
>   set to True if you wanted more detailed information on the datasets depending on paremeter 'terminal', whether you get the output in your console or as a popup
> - **data: list of Strings** <br /> 
>   list containing names of the datasets you want to store or tags for which you want to save the respective datasets
> - **tag: Boolean, default: False** <br /> 
>   set to True if data list contains tags
> - **terminal: Boolean, default: False** <br /> 
>   set to True if you want to print the meta data in your console instead of a popup

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
