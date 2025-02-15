/**

Google Earth Engine Script for the Code Editor API (JavaScript)

>>> routine for downloading Landsat 8 imagery 

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

// Function to add NDVI, NDWI, time, and constant variables to Landsat 8 imagery.
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
  .filterDate('2013-01-01', '2020-05-01') // DEFINE DATES
  .map(addVariables);

// compute the mean ndvi of the collection
//var ndvi = filteredLandsat.select('NDWI_V').reduce(ee.Reducer.mean()).clip(bbox)

var image = filteredLandsat.sort('CLOUD_COVER').first().clip(bbox);

// Display all metadata.
print('All metadata:', image);
print('Metadata:', image.get('LANDSAT_PRODUCT_ID'))
var opt_filename = ee.String("LS8_optical_").cat(image.get('DATE_ACQUIRED'));
var der_filename = ee.String("LS8_derived_").cat(image.get('DATE_ACQUIRED'));
print(opt_filename);
print(der_filename);

// Visualizar uma composicao colorida utilizando multiplas bandas
Map.addLayer(image, {min: 11000, max: 18000, bands: ['SR_B6', 'SR_B5', 'SR_B4']}, 'Composicao Landsat');
Map.addLayer(image, {min: 11000, max: 18000, bands: ['SR_B4', 'SR_B3', 'SR_B2']}, 'Composicao Landsat 2');

// Export images to drive --- comment / uncomment
// /**

// optical bands
Export.image.toDrive({
image: image.select(['SR_B6', 'SR_B5', 'SR_B4', 'SR_B3', 'SR_B2']).int16(),
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'ls8_new_optical', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
}) 

// derived indexes
Export.image.toDrive({
image: image.select(['NDVI', 'NDWI_W', 'NDWI_V']),
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'ls8_new_derived', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
}) 
// */
