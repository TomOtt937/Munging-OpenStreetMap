'''
Load the file and display the bounds of the map to assess
'''

import os
import xml.etree.cElementTree as ET
import pprint

#Update DATADIR and FILENAME as needed
DATADIR = "C:\\Users\\Home\\Documents\\TOM\\Udacity\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
#DATADIR = "C:\\Users\\Thomas\\Documents\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
FILENAME = "CentervilleArea.osm"  #  12,340K
#FILENAME = "DaytonMetro.osm"      # 110,026K

datafile = os.path.join(DATADIR, FILENAME)

osm_file = open(datafile, "r")
for event, elem in ET.iterparse(osm_file):
    if elem.tag == 'bounds':
        print elem.tag
        for attribute in elem.attrib:
            print '%s: %s' %(attribute, elem.attrib[attribute])
        break
osm_file.close()
