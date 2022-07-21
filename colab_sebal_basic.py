'''

Google Earth Engine Script for the colab API (Python)

>>> generic routine for downloading imagery 

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
'''

# [1] -- install ee
!pip install earthengine-api

# [2] -- import earth engine library
import ee

# [3] -- authenticate ee
ee.Authenticate()

# [3] -- initialize ee
ee.Initialize()

# [4] -- change working directory
import os
os.chdir('/content/drive/MyDrive/geeSEBAL-master/geeSEBAL-master/etbrasil')  # DEFINE FOLDER

# [5] -- import geesebal functions
from geesebal import Image #, Collection, TimeSeries

# [ ] -- define Landsat 8 tile id
s_tile_id = '222080'

# [ ] -- define list of dates 
# >> note there must be available scenes for such dates
lst_dates = [
'2014-11-28', 
'2014-08-08', 
'2014-07-07'
]

# [ ] -- compute ET24h and LST DEM for each scene
lst_et24h_images = list()
lst_lstdem_images = list()
lst_et24h_names = list()
lst_lstdem_names = list()
for i in range(len(lst_dates)):
    # construct image id
    print('\n>>> computing images from:')
    lcl_id = 'LANDSAT/LC08/C01/T1_SR/LC08_{}_{}'.format(s_tile_id, lst_dates[i].replace('-', ''))
    print(lcl_id)
    # get image
    lcl_lc08_image = ee.Image(lcl_id)
    lcl_sebal_image = Image(lcl_lc08_image)
    print(lcl_sebal_image)
    #print(lcl_image)
    # et
    lcl_et_image = lcl_sebal_image.image.select('ET_24h')
    print(type(lcl_et_image))
    lcl_et_name = 'LC08-C01-T1_{}_et24h_{}'.format(s_tile_id, lst_dates[i])
    print(lcl_et_name)
    lst_et24h_names.append(lcl_et_name)
    lst_et24h_images.append(lcl_et_image)
    # lst
    lcl_lst_image = lcl_sebal_image.image.select('T_LST_DEM')
    print(type(lcl_lst_image))
    lcl_lst_name = 'LC08-C01-T1_{}_lstDem_{}'.format(s_tile_id, lst_dates[i])
    print(lcl_lst_name)
    lst_lstdem_names.append(lcl_lst_name)
    lst_lstdem_images.append(lcl_lst_image)




