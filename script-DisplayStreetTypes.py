'''
This script creates a list of street types in the dataset along with a count of each.
Code reused from Udacity lesson.
'''
import os
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re

#Update DATADIR and FILENAME as needed
DATADIR = "C:\\Users\\Home\\Documents\\TOM\\Udacity\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
#DATADIR = "C:\\Users\\Thomas\\Documents\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
FILENAME = "CentervilleArea2.osm"  #  12,340K
#FILENAME = "DaytonMetro2.osm"      # 110,026K

datafile = os.path.join(DATADIR, FILENAME) 

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1
        if street_type == ',':
            print street_name

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print ("%s: %d" % (k, v))

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    osm_file = open(datafile, "r")
    audit()
    osm_file.close()
