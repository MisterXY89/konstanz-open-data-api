# Opencity

`Opencity` is an interface for the open data portal of the city of Constance.

## Capabilities
- Search by tags, name and ID
- Returns pandas DataFrame
- easy install and workflow

## Examples
### Show all available datasets
```python
from opencity import API
api = API()
api.show_data()
```

### Show all available categories
```python
api.show_categories()
# Return:
> "Geo", "Social", "Politik"...
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
