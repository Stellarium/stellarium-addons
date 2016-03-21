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

import json
import sys
import time
from utils import *

stellariumSeries = '0.15'

# checks current directory
if os.path.basename(os.getcwd()) != 'stellarium-addons':
    print('ERROR! Are you in root?')
    sys.exit(1)

# removing old catalog for the current serie
destSrc = srcPath + '/addon/' + stellariumSeries
destZip = zipPath + '/addon/'
shutil.rmtree(destSrc, ignore_errors=True)

print('--> Generating catalog: ' + stellariumSeries)

addons = {}
for root, dirs, files in os.walk(srcPath):
    for file in files:
        if file == 'info.json':
            # copy data from info.json
            with open(os.path.join(root, file)) as df:
                addon = json.load(df)
                key = addon.keys()[0]
                zipf = os.path.join(zipPath, os.path.relpath(root, srcPath) + '.zip')

                # download info
                filename = os.path.basename(zipf)
                relpath = os.path.relpath(os.path.dirname(root), srcPath)
                addon[key].update(
                        {
                            'checksum': md5(zipf),
                            'download-size': os.path.getsize(zipf),
                            'download-url': url + relpath + '/' + filename,
                            'download-filename': filename
                        }
                )

                # key must be unique
                if key in addons:
                    print('ERROR! Key is not unique! ' + root)
                    break

                # adds add-on
                addons.update(addon)
                break
            print('ERROR! Unable to load ' + root)

# append this catalog as an add-on
filename = stellariumSeries + '.zip'
addonsObj = {
    'addons':
    {
        'type': 'addon_catalog',
        'title': 'Add-ons ' + stellariumSeries,
        'date': time.strftime("%Y.%m.%d"),
        'description': 'Catalog of add-ons.',
        'supported': [stellariumSeries],
        'licence': 'GPL3',
        'license-url': 'http://www.gnu.org/licenses/gpl.html',
        'authors': [
        {
          "name": "Marcos Cardinot",
          "email": "mcardinot@gmail.com",
          "url": "http://cardinot.net"
        }
        ],
        'download-url': url + 'addon/' + filename,
        'download-filename': filename
    }
}
addons.update(addonsObj)

jsonObj = {
    'name':    'Add-ons Catalog',
    'format':  1,
    'date': time.strftime("%Y.%m.%d"),
    'series': stellariumSeries,
    'add-ons': addons
}

os.mkdir(destSrc)
jsonOut = open(destSrc + '/addons.json', 'w')
json.dump(jsonObj, jsonOut, indent=2, separators=(',', ': '))
jsonOut.close()
print('    Done! ' + jsonOut.name)


print('-> Generating the info.json file')

jsonOut = open(destSrc + '/info.json', 'w')
json.dump(addonsObj, jsonOut, indent=2, separators=(',', ': '))
jsonOut.close()
print('    Done! ' + jsonOut.name)


print('-> Generating the zip file')
compressAddons(srcPath + '/addon', destZip)
