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

# [n] -- move files to zip

import os

s_scr_dir = './content/path/folder'  # DEFINE HERE
s_file_extension = '.tif'
lst_file_markers = ['myaoi', 'ndvi']
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
      print(f)



