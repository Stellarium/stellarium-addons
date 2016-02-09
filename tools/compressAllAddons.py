# !/usr/bin/python
"""
    Marcos Cardinot <mcardinot@gmail.com>
    Copyright (C) 2016

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from  const import *
import shutil
import zipfile

def compressAddons(srcRoot, zipRoot):
    for root, dirs, files in os.walk(srcRoot):
        for addonName in dirs:
            print 'Addon: ' + addonName
            zipf = zipfile.ZipFile(os.path.join(zipRoot, addonName + '.zip'), 'w')
            for root, dirs, files in os.walk(os.path.join(srcRoot, addonName)):
                for file in files:
                    print '    ' + file
                    p = os.path.join(root, file)
                    zipf.write(p, os.path.relpath(p, os.path.join(srcRoot, '..')))
            zipf.close()

# clear zip directory
shutil.rmtree(zipPath)
os.mkdir(zipPath)

# create main folders in zip directory
for d in os.listdir(srcPath):
    srcRoot = os.path.join(srcPath, d)
    if os.path.isdir(srcRoot):
        zipRoot = os.path.join(zipPath, d)
        os.mkdir(zipRoot)
        print('\n-->Creating ' + zipRoot + '\n-------------------------------')
        compressAddons(srcRoot, zipRoot)
