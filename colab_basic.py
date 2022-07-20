# [1] -- install ee
pip install earthengine-api

# [2] -- import earth engine library
import ee

# [3] -- authenticate ee
ee.Authenticate()

# [3] -- initialize ee
ee.Initialize()

# [4] -- define the area of interest and/or bounding box
bbox = ee.Geometry.Rectangle([-51.1,-29.7, -51.0,-29.6]) # xMin, yMin, xMax, yMax.

# [5] -- access dataset
# define dataset name
s_dataset_name = 'COPERNICUS/S2_SR'  # Sentinel dataset
# get image collection in the bbox
imcol = ee.ImageCollection(s_dataset_name).filterBounds(bbox) # filter   

# [6] -- apply extra filters to dataset
# example: define date filter
imcol = imcol.filterDate('2020-01-01', '2021-01-01')
# example: define cloud filter -- 'CLOUD_COVER' for Landsat and 'CLOUDY_PIXEL_PERCENTAGE' for Sentinel
imcol = imcol.filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)

# [7] -- process dataset to output image 
# example: sort and sample first
image = imcol.sort('CLOUDY_PIXEL_PERCENTAGE').first().clip(bbox)

# [8] -- {optional} view output
from IPython.display import Image as image_display
# define pallete
mypalette = ['white', 'black']
# edit parameters
image_url = image.getThumbURL({
'min': -1, 
'max': 1, 
'palette': mypalette,
'region' : bbox,
'dimensions': 600
})
image_display(image_url, embed=True, format='png')

# [9] -- {optional} export to Drive
# edit parameters
task = ee.batch.Export.image.toDrive({
'image' : image,
'crs': 'EPSG:4326'
'description': 'myoutput',
'folder': 'ee_output', # DEFINE HERE
'fileNamePrefix' : 'output_',
'region' : bbox,
'scale' : 10, # 30 for Landsat!
'fileFormat': 'GeoTIFF'
})
# start task 
task.start()
# monitor task progress
import time 
while task.active():
        print('Polling for task (id: {}).'.format(task.id))
        time.sleep(10)
