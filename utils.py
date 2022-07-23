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

# [n] -- collect file list
import os
# define source folder
s_scr_dir = '/content/drive/MyDrive/ee_output'  # DEFINE HERE
os.chdir(s_scr_dir)
# define file extension
s_file_extension = '.tif'
# define file name markers
s_aoi_name = 'potiribu'
s_var_name = 'sr'
lst_file_markers = [s_aoi_name, s_var_name]
# get all file in the folder
lst_all_files = os.listdir(s_scr_dir)
# deploy list
lst_scr_files = list()
# colect files
for f in lst_all_files:
    b_isfile = True
    # apply extension criteria
    b_isfile = b_isfile * s_file_extension in f
    for m in lst_file_markers:
        b_isfile = b_isfile * m in f
    if b_isfile:
        #print(f)
        lst_scr_files.append('{}'.format(f))
print(len(lst_scr_files))
print(lst_scr_files[0])

# [n] -- copy to zip
from zipfile import ZipFile

# define destiny folder
s_dst_dir = '/content/drive/MyDrive/myProjects/121_paper_plans3br/inputs/datasets/potiribu'
# define zip file name
s_zipname = '{}_{}_window'.format(s_aoi_name, s_var_name)
# create a ZipFile object
zipObj = ZipFile('{}/{}.zip'.format(s_dst_dir, s_zipname), 'w')
# Add multiple files to the zip
for f in lst_scr_files:
    zipObj.write(f)
# close the Zip File
zipObj.close()

# [n] -- delete from source
s_ans = input('DANGER ZONE. Irreversible changes. Type <yes> to proceed: ')
if s_ans == 'yes':
    print('deleting files...')
    for f in lst_scr_files:
        os.remove(f)



