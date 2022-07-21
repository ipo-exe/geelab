'''

Google Earth Engine Script for the colab API (Python)

>>> routine for downloading ET and LST imagery using geesebal package 

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

# [4] -- change working directory
import os
os.chdir('/content/drive/MyDrive/geeSEBAL-master/geeSEBAL-master/etbrasil')  # DEFINE FOLDER

# [5] -- import geesebal functions
from geesebal import Image #, Collection, TimeSeries

# [6] -- define Landsat 8 tile id
s_tile_id = '222080'

# [7] -- define list of dates 
# >> note there must be available scenes for such dates
lst_dates = [
'2014-11-28', 
'2014-08-08', 
'2014-07-07'
]

# [8] -- compute images for each scenes
lst_sr_images = list()
lst_et24h_images = list()
lst_lstdem_images = list()
lst_sr_names = list()
lst_et24h_names = list()
lst_lstdem_names = list()
for i in range(len(lst_dates)):
    # construct image id
    print('\n>>> computing images from:')
    lcl_id = 'LANDSAT/LC08/C01/T1_SR/LC08_{}_{}'.format(s_tile_id, lst_dates[i].replace('-', ''))
    print(lcl_id)
    # get ee image
    lcl_lc08_image = ee.Image(lcl_id).clip(bbox) # clip image

    # select the surface reflectance bands and standardize type
    lcl_sr_image = lcl_lc08_image.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11'])
    lcl_sr_name = '{}_LC08-C01-T1_{}_sr_{}'.format(s_aoi_name, s_tile_id, lst_dates[i])
    print(type(lcl_sr_image))
    print(lcl_sr_name)
    lst_sr_names.append(lcl_sr_name)
    lst_sr_images.append(lcl_sr_image)

    # compute SEBAL image dataset
    lcl_sebal_image = Image(lcl_lc08_image)

    # et
    lcl_et_image = lcl_sebal_image.image.select('ET_24h')#.clip(bbox)
    lcl_et_name = '{}_LC08-C01-T1_{}_et24h_{}'.format(s_aoi_name, s_tile_id, lst_dates[i])
    print(type(lcl_et_image))
    print(lcl_et_name)
    lst_et24h_names.append(lcl_et_name)
    lst_et24h_images.append(lcl_et_image)

    # lst
    lcl_lst_image = lcl_sebal_image.image.select('T_LST_DEM')#.clip(bbox)
    lcl_lst_name = '{}_LC08-C01-T1_{}_lstDem_{}'.format(s_aoi_name, s_tile_id, lst_dates[i])  
    print(type(lcl_lst_image))
    print(lcl_lst_name)
    lst_lstdem_names.append(lcl_lst_name)
    lst_lstdem_images.append(lcl_lst_image)
 
# [9] -- {optional} view SR output
from IPython.display import Image as image_display
i = 0
image_url = lst_sr_images[i].select('B4').getThumbURL(
    {'min': 0, 'max': 3000, 'palette': ['white', 'red'], 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [10] -- view et output
from IPython.display import Image as image_display
et_palette = ['DEC29B', 'E6CDA1', 'EDD9A6', 'F5E4A9', 'FFF4AD', 'C3E683', '6BCC5C',
              '3BB369', '20998F', '1C8691', '16678A', '114982', '0B2C7A']
i = 0
# et
image_url = lst_et24h_images[i].getThumbURL(
    {'min': 0, 'max': 6, 'palette': et_palette, 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [11] -- view lst output
from IPython.display import Image as image_display
i = 0
image_url = lst_lstdem_images[i].getThumbURL(
    {'min': 307, 'max': 320, 'palette': ['blue', 'white', 'red'], 'dimensions': 200})
image_display(image_url, embed=True, format='png')

# [12] -- {optional} export to Drive
# use task manager for task info
# https://code.earthengine.google.com/tasks
b_reflectance = True
b_et = True
b_lst = True
# export loop
for i in range(len(lst_dates)):
    
    # retrieve objects
    s_date = lst_dates[i]
    print('\n\n::: export tasks for date: {}'.format(s_date))

    if b_reflectance:
        lcl_name = lst_sr_names[i]
        print('::: >> SR {}'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': lst_sr_images[i],
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
    if b_et:
        lcl_name = lst_et24h_names[i]
        print('>> ET24h {}'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': lst_et24h_images[i],
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
    if b_lst:
        lcl_name = lst_lstdem_names[i]
        print('>> LSTDem {}'.format(lcl_name))
        # edit parameters:
        task = ee.batch.Export.image.toDrive(**
        {
        'image': lst_lstdem_images[i],
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


