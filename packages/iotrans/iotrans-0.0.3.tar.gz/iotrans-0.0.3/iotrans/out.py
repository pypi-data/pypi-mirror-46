from shapely.geometry import mapping, MultiPolygon, MultiPoint, MultiLineString

import json
import os

import geopandas as gpd
import pandas as pd
import xmltodict

import iotrans.utils as utils


GEO_FMT = ['csv', 'geojson', 'gpkg', 'shp']
TAB_FMT = ['csv', 'json', 'xml']

MULTI_FILE = ['shp']

GEOM_TYPE_MAP = {
    'Polygon': MultiPolygon,
    'LineString': MultiLineString,
    'Point': MultiPoint
}


def supported_formats():
    '''
    Identifies the formats currently supported

    Returns:
    (set): Formats supported
    '''

    return set(GEO_FMT + TAB_FMT)

def to_file(data, path, exclude=[], projection=None, remap_shp_fields=True, zip_content=False,):
    '''
    Converts pandas DataFrame or geopandas GeoDataFrame to another format

    Parameters:
    data             (DataFrame or GeoDataFrame): Data content to be converted
    path             (str)                      : Path to the output file
    projection       (str)                      : EPSG code for the projection
    remap_shp_fields (bool)                     : If Shapefile field names should be remapped to "FILED_#" structure
    zip_content      (bool)                     : If output file should be zipped

    Returns:
    (str): Path to the converted file
    '''

    data = data[[x for x in data.columns if not x in exclude]].copy()

    filename, fmt = os.path.basename(path).split('.')
    path = os.path.dirname(path)

    fmt = fmt.lower()

    assert fmt in supported_formats(), 'Invalid output formats'
    assert (fmt in TAB_FMT and isinstance(data, (pd.DataFrame, gpd.GeoDataFrame))) or \
            (fmt in GEO_FMT and isinstance(data, gpd.GeoDataFrame)), \
            'Invalid data structure'

    # Create directory if the output format will generate multiple files (eg. Shapefile)
    if fmt in MULTI_FILE:
        path = os.path.join(path, filename) # eg. '/path/output/'

        if os.path.isdir(path):
            utils.prune(path)

        os.mkdir(path)

    output = os.path.join(path, '{0}.{1}'.format(filename, fmt))

    if fmt in GEO_FMT:
        if any([x.startswith('Multi') for x in data['geometry'].apply(lambda x: x.geom_type)]):
            data['geometry'] = data['geometry'].apply(lambda x: GEOM_TYPE_MAP[x.geom_type]([x]) if not x.geom_type.startswith('Multi') else x)

        if projection is not None:
            data = data.to_crs({ 'init': 'epsg:{0}'.format(projection) })

    if fmt in TAB_FMT and 'geometry' in data.columns:
        data['geometry'] = data['geometry'].apply(lambda x: mapping(x))

    if fmt == 'csv':
        data.to_csv(output, index=False, encoding='utf-8')
    elif fmt == 'json':
        content = data.replace({pd.np.nan: None}).to_dict(orient='records')

        with open(output, 'w') as f:
            f.write(json.dumps(content))
    elif fmt == 'xml':
        content = xmltodict.unparse({
            'DATA': {
                'ROW_{0}'.format(idx): row for idx, row in enumerate(data.to_dict('records'))
            }
        }, pretty=True)

        with open(output, 'w') as f:
            f.write(content)
    elif fmt == 'geojson':
        data.to_file(output, driver='GeoJSON', encoding='utf-8')
    elif fmt == 'gpkg':
        data.to_file(output, driver='GPKG')
    elif fmt == 'shp':
        # Map the field names to 'FIELD_#' structure to avoid field names being truncated
        if remap_shp_fields and any([len(x) > 10 for x in data.columns]):
            fields = pd.DataFrame([['FIELD_{0}'.format(i+1) if x != 'geometry' else x, x] for i, x in enumerate(data.columns)], columns=['field', 'name'])

            # Save the converted field names as a CSV in the same directory
            fields.to_csv(os.path.join(path, '{0}_fields.csv'.format(filename)), index=False, encoding='utf-8')

            data.columns = fields['field']

        data.to_file(output, driver='ESRI Shapefile')

    if zip_content:
        # Go up a directory level to zip the entire contents of the directory
        if fmt in MULTI_FILE:
            path = os.path.dirname(path)
            output = os.path.dirname(output)

        output = utils.zip_file(output, os.path.join(path, '{0}.zip'.format(filename)))

    return output
