'''
Display a specific way or node entry by ID including related tags/nodes.
'''
import os
import xml.etree.cElementTree as ET

#Update DATADIR and FILENAME as needed
DATADIR = "C:\\Users\\Home\\Documents\\TOM\\Udacity\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
#DATADIR = "C:\\Users\\Thomas\\Documents\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
FILENAME = "CentervilleArea2.osm"  #  12,340K
#FILENAME = "DaytonMetro2.osm"      # 110,026K

datafile = os.path.join(DATADIR, FILENAME) 

osm_file = open(datafile, "r")  

for event, element in ET.iterparse(osm_file):
    if element.tag == 'node' and element.attrib['id'] == "4739978993":
        for tag in element.iter():
            print tag.tag, tag.attrib
        break

osm_file.close()
