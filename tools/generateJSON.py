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
import hashlib
import json
import sys
import time

def md5(path):
    hash = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

stellariumSeries = '0.15'

# checks current directory
if os.path.basename(os.getcwd()) != 'stellarium-addons':
    print('ERROR! Are you in root?')
    sys.exit(1)

print('Generating catalog: ' + stellariumSeries)

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
                addon[key].update(
                        {
                            'checksum': md5(zipf),
                            'download-size': os.path.getsize(zipf),
                            'download-url': url + str(addon[key]['type']) + '/' + filename,
                            'download-filename': filename
                        }
                )

                # key must be unique
                if key in addons:
                    print 'ERROR! Key is not unique! ' + root
                    break

                # adds add-on
                addons.update(addon)
                break
            print 'ERROR! Unable to load ' + root

jsonObj = {
    'name':    'Add-ons Catalog',
    'format':  1,
    'version': time.strftime("%Y.%m.%d"),
    'add-ons': addons
}

jsonOut = open('catalogs/default_addons_' + stellariumSeries + '.json', 'w')
json.dump(jsonObj, jsonOut, indent=4, separators=(',', ': '))
jsonOut.close()

print('Done! ' + jsonOut.name)
