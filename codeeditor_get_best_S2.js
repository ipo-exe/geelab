/**

Google Earth Engine Script for the Code Editor API (JavaScript)

>>> routine for downloading SENTINEL 2 imagery 
- The image is the best cloud-free image from a given interval

Copyright (C) 2022 Iporã Brito Possantti
*/


// Define roi. Use the UI Drawing Tools

// Define the time range for the year.
var startDate = '2020-01-01';
var endDate = '2020-12-31';

// Load Sentinel-2 imagery for the specified time range and ROI.
var sentinelCollection = ee.ImageCollection('COPERNICUS/S2')
  .filterBounds(roi)
  .filterDate(startDate, endDate)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)); // Filter out images with more than 20% cloud cover

// Select the image with the least cloud coverage.
var bestImage = sentinelCollection.sort('CLOUDY_PIXEL_PERCENTAGE').first();

// Print the selected image.
print("Selected image:", bestImage);

// Display the selected image on the map.
Map.centerObject(roi, 10);
Map.addLayer(bestImage, {bands: ['B4', 'B3', 'B2'], max: 3000}, 'RGB');

// uncomment here for exporting
/**
// Export the best cloud-free image
Export.image.toDrive({
  image: bestImage,
  description: 'Best_Sentinel_Image_2020',
  scale: 10,
  region: roi.bounds(),
  fileFormat: 'GeoTIFF',
  crs: 'EPSG:4326',
  maxPixels: 1e13
});
*/
