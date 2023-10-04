/**

Google Earth Engine Script for the Code Editor API (JavaScript)

>>> routine for downloading DEM from Copernicus DEM asset in et-brasil

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
var bbox = aoi.bounds(); // DEFINE BUFFER or remove .buffer()

// Modelo digital de superfície Copernicus-DEM
var dem = ee.Image('projects/et-brasil/assets/anadem/v018').clip(bbox)
print(dem)

// extra options
// slope
var slope = ee.Terrain.slope(dem);

// hillshade
var exaggeration = 4;
var hillshade = ee.Terrain.hillshade(dem.multiply(exaggeration),45,45)

// ******** Visualizacao dos insumos e produtos ******** 
// Importar paletas de cores pre-definidas (https://github.com/gee-community/ee-palettes) 
var palettes = require('users/gena/packages:palettes');
// obter a paleta de cores desejada 
var palette_dem = palettes.colorbrewer.BrBG[11].reverse()
var palette_slope = palettes.colorbrewer.YlOrRd[9]

// Exibe a imagem no mapa
Map.addLayer(dem,{min: 0, max: 1000,  palette: palette_dem},'DEM')
Map.addLayer(slope, {min: 0, max: 45, palette: palette_slope}, 'Slope', true, 0.5);
Map.addLayer(hillshade, {min: 0, max: 255}, 'HS', true, 0.5);
// Export image to drive --- comment / uncomment
/**
Export.image.toDrive({
image: dem,
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'copdem_elev', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
})  
*/
/**
Export.image.toDrive({
image: slope,
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'copdem_slope', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
})  
*/
/**
Export.image.toDrive({
image: hillshade,
crs: 'EPSG:4326',
fileFormat: 'GeoTIFF',
folder: 'ee_output', // DEFINE FOLDER
description: 'copdem_hs', // DEFINE FILE NAME
region: bbox,
scale: 30,
maxPixels: 1e13
})  
*/
// ******************************************************
