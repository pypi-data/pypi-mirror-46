# iotrans

A package to easily convert structured data into various file formats

## Requirements
* Python 3.6
* geopandas>=0.4.0
* xmltodict>=0.12.0

## Installation
Using PIP via PyPI

    pip install iotrans

Manually via GIT

    git clone https://github.com/open-data-toronto/iotrans
    cd iotrans
    python setup.py install

## Usage

```python
import geopandas as gpd
import iotrans
```

### Geospatial data to XML

```python
df = gpd.read_file([data_path])
iotrans.to_file(df, './data.xml')
```
```
'./data.xml'
```

### Output as a zip file

```python
df = gpd.read_file([data_path])
iotrans.to_file(df, './data.shp')
```
```
'./data.zip'
```

## Supported Formats
### Tabular Formats
* CSV
* JSON
* XML

### Geospatial Formats
* CSV
* GeoJSON
* GeoPackage
* Shapefile

## Contribution
All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.

### Reporting issues
Please report issues [here](https://github.com/open-data-toronto/iotrans/issues).

### Contributing
Please develop in your own branch and create Pull Requests into the `dev` branch when ready for review and merge.

## License

* [MIT License](https://github.com/open-data-toronto/iotrans/blob/master/LICENSE)
