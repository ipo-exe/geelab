'''

Google Earth Engine Script for the colab API (Python)

>>> Code for retrieve and download the ANADEM Digital Elevation Model. 

This code is intended to be pasted in pieces into separate cells.

This code is distributed under GNU License v3

'''

# [cell 0] -- import modules
import ee
import time

# [cell 1] -- setups
# set file name
nm = "anadem_name" # DEFINE
# set output folder
output_folder = "content/drive/.../folder" # DEFINE

# [cell 2] -- authenticate in the gee api
ee.Authenticate()

# [cell 3] -- initialize ee
ee.Initialize(project='user_project') # DEFINE

# [cell 4] -- set Bounding box
vct_bbox = [xMin, yMin, xMax, yMax]  # this can be done using geometries and geopandas
# set the BBox object in ee
bbox = ee.Geometry.BBox(
    vct_bbox[0], # xMin
    vct_bbox[1], # yMin
    vct_bbox[2], # xMax
    vct_bbox[3] # yMax 
)   

# [cell 5] -- get a clipped ANADEM object as Image in ee
anadem = ee.Image('projects/et-brasil/assets/anadem/v1').clip(bbox)

# [cell 6] -- creat a task object for export the image to Drive
task = ee.batch.Export.image.toDrive(
    image=anadem,
    description=nm,
    folder=output_folder,
    region=bbox,
    scale=30,
    crs='EPSG:4326',
    maxPixels=1e13,
    formatOptions={'noData': -9999} # chage this if needed
)
# start task
task.start()

# monitor task progress    
while task.active():
    print('processing task id: {}'.format(s_it, task.id))
    time.sleep(20) # ajdust seconds
print("--done")
