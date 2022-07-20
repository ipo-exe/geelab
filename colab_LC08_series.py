'''

Google Earth Engine Script for the colab API (Python)

>>> generic routine for downloading LANDSAT LC08 imagery 

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

# [4] -- initialize ee
ee.Initialize()

# [5] -- define the area of interest and/or bounding box and date interval
s_aoi_name = 'myaoi'
bbox = ee.Geometry.Rectangle([-51.1,-29.65, -51.05,-29.6]) # xMin, yMin, xMax, yMax.

# [6] -- define dates intervals list 
# >> insert code for automatic list setup
lst_intervals = [
'2020-01-01',
'2020-02-01',
'2020-03-01',
'2020-04-01'
]

# [7] -- access dataset
# define dataset name -- 'LANDSAT/LC08/C02/T1_L2'
s_dataset_name = 'LANDSAT/LC08/C02/T1_L2'
# get image collection in the bbox
imcol = ee.ImageCollection(s_dataset_name).filterBounds(bbox) # filter  

# [8] -- series loop
# deploy lists
lst_names = list()
lst_dates = list()
lst_images = list()
lst_ndvi = list()
lst_ndwi_v = list()
lst_ndwi_w = list()
for i in range(1, len(lst_intervals)):    
    # retrieve dates
    s_date_end = lst_intervals[i]
    s_date_start = lst_intervals[i - 1]
    print('\n Interval: {} to {}'.format(s_date_end, s_date_start))

    # -- apply extra filters to local dataset
    # example: define date filter
    imcol_lcl = imcol.filterDate(s_date_start, s_date_end)
    # example: define cloud filter -- 'CLOUD_COVER' for Landsat and 'CLOUDY_PIXEL_PERCENTAGE' for Sentinel
    imcol_lcl = imcol_lcl.filterMetadata('CLOUD_COVER', 'less_than', 50)
    n_images = imcol_lcl.size().getInfo()
    print('>> {} images found'.format(n_images))
    if n_images == 0:
        pass
    else:
        # -- process dataset to output called image 
        # sort and sample first and clip
        image = imcol_lcl.sort('CLOUD_COVER').first().clip(bbox)
        # select the bands
        image = image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7', 'ST_B10'])
        lst_images.append(image)
        
        # ndvi option:
        b_ndvi = False
        if b_ndvi:
            nir = image.select('SR_B5')
            red = image.select('SR_B4')
            ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
            lst_ndvi.append(ndvi)
        # ndwi_w option:
        b_ndwi_w = False
        if b_ndwi_w:
            green = image.select('SR_B3')
            nir = image.select('SR_B5')
            ndwi_w = green.subtract(nir).divide(nir.add(green)).rename('NDWIw')
            lst_ndwi_w.append(ndwi_w)
        # ndwi_v option:
        b_ndwi_v = False
        if b_ndwi_v:
            nir = image.select('SR_B5')
            swir = image.select('SR_B6')
            ndwi_v = nir.subtract(swir).divide(nir.add(swir)).rename('NDWIv')
            lst_ndwi_v.append(ndwi_v)
        
        # -- retrieve metadata from image
        dct_meta = dict(image.getInfo())
        s_id_full = dct_meta['id']
        s_name_image = s_id_full.split('/')[-1][:11]
        print('>> selected:')
        print(s_id_full)
        print(s_name_image)
        # Get the timestamp.
        ee_date = ee.Date(image.get('system:time_start'))
        # convert to human readable date with ee.Date.format().
        s_date = ee_date.format().getInfo()[:10]
        print(s_date)
        lst_names.append(s_name_image)
        lst_dates.append(s_date)
    
# [9] -- {optional} view output
from IPython.display import Image as image_display
# define pallete
mypalette = ['white', 'black']
# edit parameters
image_url = lst_images[0].select('SR_B4').getThumbURL({
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
b_reflectance = True
# export loop
for i in range(len(lst_images)):
    
    # retrieve objects
    s_name_image = lst_names[i]
    s_date = lst_dates[i]
    print('\n\n >>{} - {}'.format(s_name_image, s_date))
    image = lst_images[i]
    
    if b_reflectance:
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': image,
        'crs': 'EPSG:4326',
        'description': '{}_sr_{}_{}'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('Polling for task (id: {}).'.format(task.id))
                time.sleep(10)
    # ndvi option:
    if b_ndvi:
        print('** NDVI **')
        ndvi = lst_ndvi[i]
        task = ee.batch.Export.image.toDrive(**
        {
        'image': ndvi,
        'crs': 'EPSG:4326',
        'description': '{}_ndvi_{}_{}'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('Polling for task (id: {}).'.format(task.id))
                time.sleep(10)
    # ndwi_w option:
    if b_ndwi_w:
        print('** NDWI-W **')
        ndwi_w = lst_ndwi_w[i]
        task = ee.batch.Export.image.toDrive(**
        {
        'image': ndwi_w,
        'crs': 'EPSG:4326',
        'description': '{}_ndwi-w_{}_{}'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('Polling for task (id: {}).'.format(task.id))
                time.sleep(10)
    # ndwi_v option:
    if b_ndwi_v:
        print('** NDWI-V **')
        ndwi_v = lst_ndwi_v[i]
        task = ee.batch.Export.image.toDrive(**
        {
        'image': ndwi_v,
        'crs': 'EPSG:4326',
        'description': '{}_ndwi-v_{}_{}'.format(s_aoi_name, s_name_image, s_date), # DEFINE HERE
        'folder': 'ee_output', # DEFINE HERE
        'region' : bbox,
        'scale' : 30, # 30 for Landsat and 10 for Sentinel
        })
        # start task 
        task.start()
        # monitor task progress
        import time 
        while task.active():
                print('Polling for task (id: {}).'.format(task.id))
                time.sleep(10)
