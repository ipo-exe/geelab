'''

Google Earth Engine Script for the colab API (Python)

>>> generic routine for downloading LS8 imagery 

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

# [4] -- define the area of interest and/or bounding box
bbox = ee.Geometry.Rectangle([-51.1,-29.7, -51.0,-29.6]) # xMin, yMin, xMax, yMax.

# [5] -- access dataset
# define dataset name -- 'LANDSAT/LC08/C02/T1_L2'
s_dataset_name = 'LANDSAT/LC08/C02/T1_L2'
# get image collection in the bbox
imcol = ee.ImageCollection(s_dataset_name).filterBounds(bbox) # filter   

# [6] -- apply extra filters to dataset
# example: define date filter
imcol = imcol.filterDate('2020-01-01', '2021-01-01')
# example: define cloud filter -- 'CLOUD_COVER' for Landsat and 'CLOUDY_PIXEL_PERCENTAGE' for Sentinel
imcol = imcol.filterMetadata('CLOUD_COVER', 'less_than', 10)

# [7] -- process dataset to output image 
# example: sort and sample first
image = imcol.sort('CLOUDY_PIXEL_PERCENTAGE').first().clip(bbox)
# example: select the bands
image = image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6'])
ndvi = 

# [8] -- {optional} view output
from IPython.display import Image as image_display
# define pallete
mypalette = ['white', 'black']
# edit parameters
image_url = image.select('SR_B4').getThumbURL({
'min': 0, # edit
'max': 15000, # edit
'palette': mypalette,
'region' : bbox,
'dimensions': 300
})
image_display(image_url, embed=True, format='png')

# [9] -- {optional} export to Drive
# use task manager for task info
# https://code.earthengine.google.com/tasks
# edit parameters:
task = ee.batch.Export.image.toDrive(**
{
'image': image,
'crs': 'EPSG:4326',
'description': 'colab_output_ls8',  # edit
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
