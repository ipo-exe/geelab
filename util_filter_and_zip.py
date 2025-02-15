'''

Google Earth Engine Script for the colab API (Python)

>>> utility routines

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

# [n] -- import 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# [n] -- import from planslab
import visuals

# [n] -- collect date list
import os
# define source folder
s_scr_dir = '/content/drive/.../folder'  # DEFINE HERE
os.chdir(s_scr_dir)
# define file extension
s_file_extension = '.tif'
# define file name markers
s_aoi_name = 'potiribu'
s_var_name = 'et24h'
# get all file in the folder
lst_all_files = os.listdir(s_scr_dir)
# deploy list
lst_scr_dates = list()
# colect files
for f in lst_all_files:
    # apply extension criteria
    if f[-4:] == s_file_extension:
        if s_aoi_name in f and s_var_name in f:
            print(f)  
            im = Image.open(f)
            grd = np.array(im)
            n_grd_size = len(grd) * len(grd[0])
            grd_nan = np.isnan(grd).sum()
            r_nan_ratio = grd_nan.sum() / n_grd_size
            print(r_nan_ratio)
            if r_nan_ratio < 0.1:
                s_lcl_date = f.split('_')[-1].split('.')[0]
                print(s_lcl_date)
                lst_scr_dates.append(s_lcl_date)   
            else:
                print('passed')            
print(len(lst_scr_dates))

# [n] -- copy to zip
from zipfile import ZipFile
# define destiny folder
s_dst_dir = '/content/drive/.../folder'

# [n] --  plot and zip 
# define source folder
s_scr_dir = '/content/drive/.../folder'  # DEFINE HERE
os.chdir(s_scr_dir)
# define file extension
s_file_extension = '.tif'
# define file name markers
lst_var_names = ['et24h', 'ndvi', 'lstDem', 'sr']
lst_var_cmaps = ['flow_v', 'ndvi', 'lst']
lst_ranges = [(0, 10), (0, 1), (290, 320)]
for i in range(len(lst_var_names)):
    s_var_name = lst_var_names[i]
    print(s_var_name)
    # define zip file name
    s_zipname = '{}_{}_window_teste3'.format(s_aoi_name, s_var_name)
    # create a ZipFile object
    zipObj = ZipFile('{}/{}.zip'.format(s_dst_dir, s_zipname), 'w')
    for f in lst_all_files:
        for d in lst_scr_dates:
            # apply extension criteria
            if f[-4:] == s_file_extension:
                if s_aoi_name in f and s_var_name in f and d in f:
                    print(f)
                    # write images
                    zipObj.write(f)
                    lcl_file_name = f.split('.')[0]
                    print(lcl_file_name)
                    lcl_view_file = 'view_{}'.format(lcl_file_name)
                    if s_var_name == 'sr':
                        pass
                    else:
                        im = Image.open(f)
                        grd = np.array(im)
                        visuals.plot_map_view(
                            grd_map2d=grd, 
                            dct_meta={},
                            tpl_ranges=lst_ranges[i],
                            s_mapid=lst_var_cmaps[i],
                            s_mapttl='{} | {}'.format(s_var_name, d),
                            s_file_name=lcl_view_file,
                            s_dir_out=s_scr_dir,
                            b_metadata=False,
                            b_show=False,
                            b_integration=False,
                            b_png=False,
                            )
                        print(lcl_view_file)
                        zipObj.write('{}.jpg'.format(lcl_view_file))       
    # close the Zip File
    zipObj.close()

