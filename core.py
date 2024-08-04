import ee
import geemap
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Get the current and next year
current_year = datetime.now().year
next_year = current_year + 1

# define default datasets
datasets = {
  "Landsat 9": "LANDSAT/LC09/C02/T1_L2",
	"Landsat 8": "LANDSAT/LC08/C02/T1_L2",
	"Landsat 7": "LANDSAT/LE07/C02/T1_L2",
	"Landsat 5": "LANDSAT/LT05/C02/T1_L2",
  "Sentinel 2": "COPERNICUS/S2_SR_HARMONIZED",
  # todo handle others like Landsat 4, 3, 2 and MODIS
}

# define cloud cover attribute
cloud_cover = {
  "Landsat 9": "CLOUD_COVER",
	"Landsat 8": "CLOUD_COVER",
	"Landsat 7": "CLOUD_COVER",
	"Landsat 5": "CLOUD_COVER",
  "Sentinel 2": "CLOUDY_PIXEL_PERCENTAGE",
  # todo handle others like Landsat 4, 3, 2 and MODIS
}

# define dates
dates = [
  "1970-01-01", # baseline date
  "{}-01-01".format(next_year)  
]

# ASSESSMENT TOOL
def assess_image_catalog(
  roi, # list with [xmin, ymin, xmax, ymax]
  dataset, # key for dataset
  start=None,
  end=None,
  talk=True
):  
    # Hande Nones
    if start is None:
        start = dates[0]
    if end is None:
        end = dates[1]

    if talk:
        print("{} from {} to {} in {}".format(dataset, start, end, roi))

    # Get Bbox
    if talk:
        print(" --- getting bounding box...")
    bbox = ee.Geometry.Rectangle(roi)

    # Define the date range
    if talk:
        print(" --- getting date range...")
    dt_range = ee.DateRange(start, end)

    # get image collection
    if talk:
        print(" --- getting image collection...")
    im_coll = (ee.ImageCollection(datasets[dataset]).filterDate(dt_range).filterBounds(bbox))

    # handle void list
    try:
        # retrieve image
        image_list = im_coll.toList(im_coll.size())      
        size = image_list.size().getInfo()
        if talk:
            print(" --- {} images found".format(size))

        # loop in image list
        ls_date = []
        ls_cloud = []
        ls_id = []
        for i in range(size):
            # get image
            image = ee.Image(image_list.get(i))
            image_id = image.id().getInfo()
            image_date = image.date().format('YYYY-MM-dd').getInfo()
            cloud_coverage = image.get(cloud_cover[dataset]).getInfo()
            if talk:
                print(" --- {}/{} -- {} {} {}".format(
                i + 1, 
                size,
                image_id,
                image_date,
                cloud_coverage
                )
                )
            # collect metadata
            ls_id.append(image_id)
            ls_date.append(image_date)
            ls_cloud.append(cloud_coverage)
            
        # return dataframe
        df = pd.DataFrame(
            {
            "ImageID": ls_id,
            "Date": ls_date,
            "CloudCover%": ls_cloud
            }
        )
        # extra constant columns
        df["Dataset"] = dataset
        df["DatasetID"] = datasets[dataset]
        return df
            
    except:
        if talk:
            print("No images found")
        return 0

  
  



  
  
  
