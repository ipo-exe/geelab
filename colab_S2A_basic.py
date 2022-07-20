'''

Google Earth Engine Script for the colab API (Python)

>>> generic routine for downloading Sentinel-2 MSI: MultiSpectral Instrument, Level-2A imagery 

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

If not, see <https://www.gnu.org/licenses/>.
'''

# [1] -- install ee
!pip install earthengine-api

# [2] -- import earth engine library
import ee

# [3] -- authenticate ee
ee.Authenticate()

# [3] -- initialize ee
ee.Initialize()

# [4] -- define the area of interest and/or bounding box and date interval
s_aoi_name = 'myaoi'
bbox = ee.Geometry.Rectangle([-51.1,-29.7, -51.0,-29.6]) # xMin, yMin, xMax, yMax.
s_date_start = '2020-01-01'
s_date_end = '2021-01-01'

# [5] -- access dataset
# define dataset name
s_dataset_name = 'COPERNICUS/S2_SR'
# get image collection in the bbox
imcol = ee.ImageCollection(s_dataset_name).filterBounds(bbox) # filter   

# [6] -- apply extra filters to dataset
# example: define date filter
imcol = imcol.filterDate(s_date_start, s_date_end)
# example: define cloud filter --'CLOUDY_PIXEL_PERCENTAGE' for Sentinel
imcol = imcol.filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)

# [7] -- process dataset to output called image 
# sort and sample first and clip
image = imcol.first().clip(bbox) #sort('CLOUDY_PIXEL_PERCENTAGE').
# select the bands
image = image.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])

# ndvi option:
b_ndvi = True
if b_ndvi:
    nir = image.select('B8')
    red = image.select('B4')
    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
# ndwi_w option:
b_ndwi_w = True
if b_ndwi_w:
    green = image.select('B3')
    nir = image.select('B8')
    ndwi_w = green.subtract(nir).divide(nir.add(green)).rename('NDWIw')
# ndwi_v option:
b_ndwi_v = True
if b_ndwi_v:
    nir = image.select('B8')
    swir = image.select('B12')
    ndwi_v = nir.subtract(swir).divide(nir.add(swir)).rename('NDWIv')

# [8] -- retrieve metadata from image
dct_meta = dict(image.getInfo())
s_id_full = dct_meta['id']
s_name_image = 'S2A_' + s_id_full.split('_')[-1]
print(s_id_full)
print(s_name_image)
# Get the timestamp.
ee_date = ee.Date(image.get('system:time_start'))
# convert to human readable date with ee.Date.format().
s_date = ee_date.format().getInfo()[:10]
print(s_date)

# [9] -- {optional} view output
from IPython.display import Image as image_display
# define pallete
mypalette = ['white', 'black']
# edit parameters
image_url = image.select('B4').getThumbURL({
'min': 0, # edit
'max': 15000, # edit
'palette': mypalette,
'region' : bbox,
'dimensions': 300
})
image_display(image_url, embed=True, format='png')

# [10] -- {optional} export to Drive
# use task manager for task info
# https://code.earthengine.google.com/tasks
# edit parameters:
task = ee.batch.Export.image.toDrive(**
{
'image': image,
'crs': 'EPSG:4326',
'description': '{}_{}_{}_reflectance'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
'folder': 'ee_output', # DEFINE HERE
'region' : bbox,
'scale' : 10, # 30 for Landsat and 10 for Sentinel
})
# start task 
task.start()
# monitor task progress
import time 
while task.active():
        print('Polling for task (id: {}).'.format(task.id))
        time.sleep(10)
# ndvi option:
b_ndvi = True
if b_ndvi:
    print('** NDVI **')
    task = ee.batch.Export.image.toDrive(**
    {
    'image': ndvi,
    'crs': 'EPSG:4326',
    'description': '{}_{}_{}_ndvi'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
    'folder': 'ee_output', # DEFINE HERE
    'region' : bbox,
    'scale' : 10, # 30 for Landsat and 10 for Sentinel
    })
    # start task 
    task.start()
    # monitor task progress
    import time 
    while task.active():
            print('Polling for task (id: {}).'.format(task.id))
            time.sleep(10)
# ndwi_w option:
b_ndwi_w = True
if b_ndwi_w:
    print('** NDWI-W **')
    task = ee.batch.Export.image.toDrive(**
    {
    'image': ndwi_w,
    'crs': 'EPSG:4326',
    'description': '{}_{}_{}_ndwi-w'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
    'folder': 'ee_output', # DEFINE HERE
    'region' : bbox,
    'scale' : 10, # 30 for Landsat and 10 for Sentinel
    })
    # start task 
    task.start()
    # monitor task progress
    import time 
    while task.active():
            print('Polling for task (id: {}).'.format(task.id))
            time.sleep(10)
# ndwi_v option:
b_ndwi_v = True
if b_ndwi_v:
    print('** NDWI-V **')
    task = ee.batch.Export.image.toDrive(**
    {
    'image': ndwi_v,
    'crs': 'EPSG:4326',
    'description': '{}_{}_{}_ndwi-v'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
    'folder': 'ee_output', # DEFINE HERE
    'region' : bbox,
    'scale' : 10, # 30 for Landsat and 10 for Sentinel
    })
    # start task 
    task.start()
    # monitor task progress
    import time 
    while task.active():
            print('Polling for task (id: {}).'.format(task.id))
            time.sleep(10)
