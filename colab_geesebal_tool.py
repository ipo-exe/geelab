'''

Google Earth Engine Script for the colab API (Python)

>>> tool for downloading ET and LST imagery using geesebal package 

Copyright (C) 2022 Iporã Brito Possantti

************ GNU GENERAL PUBLIC LICENSE ************

https://www.gnu.org/licenses/gpl-3.0.en.html
Permissions:
 - Commercial use
 - Distribution
 - Modification
 - Patent use
 - Private use
Conditions:
 - Disclose source
 - License and copyright notice
 - Same license
 - State changes
Limitations:
 - Liability
 - Warranty
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  

If not, see <https://www.gnu.org/licenses/>

'''

# [1] -- install ee
!pip install earthengine-api

# [2] -- import earth engine library
import ee

# [3] -- authenticate ee
ee.Authenticate()

# [4] -- initialize ee
ee.Initialize()

# [5] -- change working directory
import os
os.chdir('/content/drive/MyDrive/geeSEBAL-master/geeSEBAL-master/etbrasil')  # DEFINE FOLDER

# [6] -- import geesebal functions
from geesebal import Image #, Collection, TimeSeries

# [7] -- install geopandas
!pip install geopandas

# [8] -- import geopandas
import geopandas as gpd

# [9] -- read geodataframe
s_file_aois = '/content/drive/MyDrive/myProjects/121_paper_plans3br/inputs/datasets/plans3br_aois_windows.gpkg'
gdf_aois = gpd.read_file(s_file_aois, layer='plans3br_aois_window')
print(gdf_aois.to_string())

# [10] -- define the area of interest and/or bounding box and date interval
s_aoi_name = 'planalto' # gdf_aois['aoi'].values[a]
gdf_aoi = gdf_aois.query('aoi == "{}"'.format(s_aoi_name))
vct_bbox = gdf_aoi.bounds.values[0]
print(vct_bbox)
bbox = ee.Geometry.Rectangle([vct_bbox[0], 
                              vct_bbox[1],
                              vct_bbox[2],
                              vct_bbox[3]]) # xMin, yMin, xMax, yMax.

# [11] -- define dates intervals list 
import pandas as pd
s_date_start = '2020-06-01'
s_date_end = '2020-08-01'
dtrng = pd.date_range(start=s_date_start, end=s_date_end, freq='SMS')
lst_intervals = list()
for i in range(len(dtrng)):
    lst_intervals.append(str(dtrng.values[i])[:10])
for d in lst_intervals:
    print(d)

# [12] -- access dataset
# define dataset name -- 
s_dataset_name = 'LANDSAT/LC08/C01/T1_SR'
# get image collection in the bbox
imcol = ee.ImageCollection(s_dataset_name).filterBounds(bbox) # filter  

# [13] -- define processing options
b_sr = False
b_ndvi = True
b_ndwi_w = False
b_ndwi_v = False
b_geesebal = False
b_et24h = False
b_lst = False

# [14] -- series loop
# deploy dicts
dct_sr_images = dict()
dct_ndvi_images = dict()
dct_ndwiw_images = dict()
dct_ndwiv_images = dict()
dct_et_images = dict()
dct_lst_images = dict()

# [15] -- processing loop
for i in range(1, len(lst_intervals)):    
    # retrieve dates
    s_date_end = lst_intervals[i]
    s_date_start = lst_intervals[i - 1]
    print('\n Interval: {} to {}'.format(s_date_start, s_date_end,))

    # -- apply extra filters to local dataset
    # example: define date filter
    imcol_lcl = imcol.filterDate(s_date_start, s_date_end)
    # example: define cloud filter -- 'CLOUD_COVER' for Landsat and 'CLOUDY_PIXEL_PERCENTAGE' for Sentinel
    imcol_lcl = imcol_lcl.filterMetadata('CLOUD_COVER', 'less_than', 50)
    
    # image counting
    n_images = imcol_lcl.size().getInfo()
    print('>> {} images found'.format(n_images))
    
    if n_images == 0:
        pass
    else:
        # -- process image dataset
        # sort and sample first and clip
        image = imcol_lcl.sort('CLOUD_COVER').first().clip(bbox)

        # -- retrieve metadata from image
        dct_meta = dict(image.getInfo())
        s_id_full = dct_meta['id']
        s_id_tile = s_id_full.split('_')[-2]
        s_aux = s_id_full.split('_')[-1]
        s_date = s_aux[:4] + '-' + s_aux[4:6] + '-' + s_aux[6:]
        s_prefix = 'LC08-C01-T1SR_' + s_id_tile
        print('>> selected:')
        print(s_id_full)
        print('prefix : {}'.format(s_prefix))
        print('date : {}'.format(s_date))

        # sr option
        if b_sr:
            # select the bands
            image_sr = image.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11'])
            dct_sr_images['{}_sr_{}'.format(s_prefix, s_date)] = image_sr
        
        # ndvi option:
        if b_ndvi:
            nir = image.select('B5')
            red = image.select('B4')
            ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
            dct_ndvi_images['{}_ndvi_{}'.format(s_prefix, s_date)] = ndvi
        
        # ndwi_w option:
        if b_ndwi_w:
            green = image.select('B3')
            nir = image.select('B5')
            ndwi_w = green.subtract(nir).divide(nir.add(green)).rename('NDWIw')
            dct_ndwiw_images['{}_ndwi-w_{}'.format(s_prefix, s_date)] = ndwi_w
        
        # ndwi_v option:
        if b_ndwi_v:
            nir = image.select('B5')
            swir = image.select('B6')
            ndwi_v = nir.subtract(swir).divide(nir.add(swir)).rename('NDWIv')
            dct_ndwiv_images['{}_ndwi-v_{}'.format(s_prefix, s_date)] = ndwi_v   
        
        # geeSebal option
        if b_geesebal:
            # compute SEBAL image dataset
            sebal_image = Image(image)  
            print(sebal_image)
            
            # ET24h product:
            if b_et24h:
                et_image = sebal_image.image.select('ET_24h')
                dct_et_images['{}_et24h_{}'.format(s_prefix, s_date)] = et_image 
            
            # LST product:
            if b_lst:
                lst_image = sebal_image.image.select('T_LST_DEM')
                dct_lst_images['{}_lstDem_{}'.format(s_prefix, s_date)] = lst_image

# [ ] -- {optional} view SR output
from IPython.display import Image as image_display
# grab keys 
lst_k = list()
for k in dct_sr_images:
    lst_k.append(k)
    print(k)
image_url = dct_sr_images[lst_k[0]].select('B4').getThumbURL(
    {'min': 0, 'max': 3000, 'palette': ['white', 'red'], 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [ ] -- {optional} view NDVI output
from IPython.display import Image as image_display
# grab keys 
lst_k = list()
for k in dct_ndvi_images:
    lst_k.append(k)
image_url = dct_ndvi_images[lst_k[1]].select('NDVI').getThumbURL(
    {'min': 0.3, 'max': 0.8, 'palette': ['white', 'green'], 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [ ] -- {optional} view NDWI-V output
from IPython.display import Image as image_display
# grab keys 
lst_k = list()
for k in dct_ndwiv_images:
    lst_k.append(k)
image_url = dct_ndwiv_images[lst_k[1]].select('NDWIv').getThumbURL(
    {'min': 0, 'max': 0.8, 'palette': ['white', 'green'], 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [ ] -- {optional} view ET output
from IPython.display import Image as image_display
# grab keys 
lst_k = list()
for k in dct_et_images:
    lst_k.append(k)
    print(k)
et_palette = ['DEC29B', 'E6CDA1', 'EDD9A6', 'F5E4A9', 'FFF4AD', 'C3E683', '6BCC5C',
              '3BB369', '20998F', '1C8691', '16678A', '114982', '0B2C7A']
image_url = dct_et_images[lst_k[0]].getThumbURL(
    {'min': 0, 'max': 6, 'palette': et_palette, 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [ ] -- {optional} view ET output
from IPython.display import Image as image_display
# grab keys 
lst_k = list()
for k in dct_lst_images:
    lst_k.append(k)
image_url = dct_lst_images[lst_k[0]].getThumbURL(
    {'min': 300, 'max': 320, 'palette': ['blue', 'white', 'red'], 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [ ] -- {optional} export to Drive
# use task manager for task info
# https://code.earthengine.google.com/tasks

# [ ] -- SR output
if b_sr:
    for k in dct_sr_images:
        lcl_name = s_aoi_name + '_' + k
        print('\n::: >> SR {} :::'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': dct_sr_images[k],
        'crs': 'EPSG:4326',
        'description': lcl_name, 
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('::: running task (id: {}).'.format(task.id))
                time.sleep(10)
# [ ] -- NDVI output
if b_ndvi:
    for k in dct_ndvi_images:
        lcl_name = s_aoi_name + '_' + k
        print('\n::: >> NDVI {} :::'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': dct_ndvi_images[k].toFloat(),
        'crs': 'EPSG:4326',
        'description': lcl_name, 
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('::: running task (id: {}).'.format(task.id))
                time.sleep(10)

# [ ] -- NDWI-V output
if b_ndwi_v:
    for k in dct_ndwiv_images:
        lcl_name = s_aoi_name + '_' + k
        print('\n::: >> NDWI-V {} :::'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': dct_ndwiv_images[k].toFloat(),
        'crs': 'EPSG:4326',
        'description': lcl_name, 
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('::: running task (id: {}).'.format(task.id))
                time.sleep(10)

# [ ] -- NDWI-W output
if b_ndwi_w:
    for k in dct_ndwiw_images:
        lcl_name = s_aoi_name + '_' + k
        print('\n::: >> NDWI-W {} :::'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': dct_ndwiw_images[k].toFloat(),
        'crs': 'EPSG:4326',
        'description': lcl_name, 
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('::: running task (id: {}).'.format(task.id))
                time.sleep(10)
 
# [ ] -- ET output
if b_et24h:
    for k in dct_et_images:
        lcl_name = s_aoi_name + '_' + k
        print('\n::: >> ET 24h {} :::'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': dct_et_images[k].toFloat(),
        'crs': 'EPSG:4326',
        'description': lcl_name, 
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('::: running task (id: {}).'.format(task.id))
                time.sleep(10)

# [ ] -- LST output
if b_lst:
    for k in dct_lst_images:
        lcl_name = s_aoi_name + '_' + k
        print('\n::: >> LST DEM {} :::'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': dct_lst_images[k].toFloat(),
        'crs': 'EPSG:4326',
        'description': lcl_name, 
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('::: running task (id: {}).'.format(task.id))
                time.sleep(10)
