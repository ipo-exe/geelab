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
