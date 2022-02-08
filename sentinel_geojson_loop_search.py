import os
from datetime import datetime, timedelta

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from sentinelsat.sentinel import SentinelAPI, geojson_to_wkt, read_geojson

#Credentials for Sentinel Copernicus Hub
user = '' ## change this!
password = '' ## change this!

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

directory = r"marine-debris-geojsons"

id_list = []

for root, dirs, files in os.walk(os.path.abspath(directory)):
    for file in files:
        if file.endswith(".geojson"):
            file_path = os.path.join(root, file)
            
            try:
                #Use existing geojson or create one on geojson.io
                debris_date = file.split('_')[1]
                format = '%Y-%m-%d'
                date_object = datetime.strptime(debris_date, format)
                start_date = date_object - timedelta(14)
                end_date = date_object + timedelta(14)
                start_date = start_date.strftime('%Y%m%d')
                end_date = end_date.strftime('%Y%m%d')

                footprint = geojson_to_wkt(read_geojson(file_path))
                #print(footprint)
                
                products = api.query(footprint,
                     date = (start_date, end_date),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 20))
                
                areas = api.to_geodataframe(products)
                product_details = api.to_geodataframe(products)
                sentinel_id = product_details.title[1]
                id_list.append(sentinel_id)
                #print(sentinel_id)

            
            except:
                pass

print(id_list)
