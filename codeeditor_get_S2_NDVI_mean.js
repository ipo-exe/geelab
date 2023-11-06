/**

Google Earth Engine Script for the Code Editor API (JavaScript)

>>> routine for downloading mean NDVI from SENTINEL 2 imagery 
- The derived NDVI is the reduced mean for a time interval

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
*/

// Define roi. Use the UI Drawing Tools

// Define the time range for the year.
var startDate = '2020-01-01';
var endDate = '2020-12-31';

// Load Sentinel-2 imagery for the specified time range and ROI.
var sentinelCollection = ee.ImageCollection('COPERNICUS/S2')
  .filterBounds(roi)
  .filterDate(startDate, endDate);

// Calculate NDVI for each image in the collection.
var calculateNDVI = function(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
};

var sentinelCollectionWithNDVI = sentinelCollection.map(calculateNDVI);

// Calculate the mean NDVI for the entire year 2020 within the ROI.
var meanNDVI = sentinelCollectionWithNDVI.select('NDVI')
  .reduce(ee.Reducer.mean());

// Print the result.
print("Mean NDVI for 2020:", meanNDVI);

// Display the mean NDVI on the map.
// /**
Map.centerObject(roi, 15);
Map.addLayer(meanNDVI, {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
}, 'Mean NDVI');
// */

// Export image to drive --- comment / uncomment
// /**
Export.image.toDrive({
image: meanNDVI,
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'S2ndvi_2020_mean', // DEFINE FILE NAME
region: roi.bounds(),
scale: 10,
maxPixels: 1e13
}) 
// */
