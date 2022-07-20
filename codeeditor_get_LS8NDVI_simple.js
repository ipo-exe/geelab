/**

Google Earth Engine Script for the Code Editor API (JavaScript)

>>> routine for downloading NDVI from Landsat 8 imagery 
- The derived NDVI is the reduced mean for a time interval
- You may change for downloading NDWI_W and NDWI_V

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

// Define aoi. Use the UI Drawing Tools

// get bounding box using buffer (in meters)
var bbox = aoi.buffer(1500).bounds(); // DEFINE BUFFER

// Function to cloud mask from the pixel_qa band of Landsat 8 SR data.
var maskL8sr = function(image) {
  // Bit 0 - Fill
  // Bit 1 - Dilated Cloud
  // Bit 2 - Cirrus
  // Bit 3 - Cloud
  // Bit 4 - Cloud Shadow
  var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
  var saturationMask = image.select('QA_RADSAT').eq(0);

  // Apply the scaling factors to the appropriate bands.
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);

  // Replace the original bands with the scaled ones and apply the masks.
  return image.addBands(opticalBands, null, true)
    .addBands(thermalBands, null, true)
    .updateMask(qaMask)
    .updateMask(saturationMask);
};

// Function to add NDVI, time, and constant variables to Landsat 8 imagery.
var addVariables = function(image) {
  // Compute time in fractional years since the epoch.
  var date = image.date();
  var years = date.difference(ee.Date('1970-01-01'), 'year');
  // Return the image with the added bands.
  return image
  // Add an NDVI band.
  .addBands(image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI'))
  // Add an NDWI water band
  .addBands(image.normalizedDifference(['SR_B3','SR_B5']).rename('NDWI_W'))
  // Add an NDWI veg band
  .addBands(image.normalizedDifference(['SR_B5','SR_B6']).rename('NDWI_V'))
  // Add a time band.
  .addBands(ee.Image(years).rename('time')).float()
  // Add a constant band.
  .addBands(ee.Image.constant(1));
};

// Get image collection
var landsat8Sr = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")

// Remove clouds, add variables and filter to the area of interest.
var filteredLandsat = landsat8Sr
  .filterBounds(bbox)
  .filterMetadata('CLOUD_COVER', 'less_than', 10) // DEFINE CLOUD % CRITERIA
  .filterDate('2010', '2020') // DEFINE DATES
  .map(maskL8sr)
  .map(addVariables);

// compute the mean ndvi of the collection
var ndvi = filteredLandsat.select('NDVI').reduce(ee.Reducer.mean()).clip(bbox)

// add ndvi mean
Map.addLayer(ndvi,
  {bands: 'NDVI_mean',
  min: 0.1, max: 0.9, palette: ['white', 'green']},
  'NDVI Mosaic');

// Export image to drive --- comment / uncomment
// /**
Export.image.toDrive({
image: ndvi,
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'ls8ndvi', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
}) 
// */

// ******************************************************
