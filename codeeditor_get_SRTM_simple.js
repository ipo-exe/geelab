/**

Google Earth Engine Script for the Code Editor API (JavaScript)

>>> routine for downloading DEM from SRTM imagery 

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
var bbox = aoi.buffer(1500).bounds(); // DEFINE BUFFER or remove .buffer()

// get SRTM
var srtm = ee.Image("USGS/SRTMGL1_003").clip(bbox)

// ******** Visualizacao dos insumos e produtos ******** 
// Importar paletas de cores pre-definidas (https://github.com/gee-community/ee-palettes) 
var palettes = require('users/gena/packages:palettes');
// obter a paleta de cores desejada 
var palette = palettes.colorbrewer.BrBG[11].reverse()
// add to map

Map.addLayer(srtm,{min: 0, max: 600,  palette: palette},'SRTM')    

// Export image to drive --- comment / uncomment
// /**
Export.image.toDrive({
image: srtm,
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'srtm_new', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
})  
// */
// ******************************************************
