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

'''
Update unwanted street types to the expected version.  Deal with Unicode entries.
Code adapted from the Udacity lesson.
'''
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# Add abreviation changes to make here
mapping = { "Ave": "Avenue",
            "Blvd": "Boulevard",
            "Cir": "Circle",
            "Ct": "Court",
            "Dr": "Drive",
            "Rd.": "Road",
            "Rd": "Road",          
            "St": "Street",
            "St,": "Street",           
            "St.": "Street"
            }

def audit_street_type(street_types, street_name): 
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    osm_file = open(datafile, "r")
    
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def update_name(name, mapping):
    for word in name.split(" "):
        #print (word)
        if word in mapping:
            #print (mapping[word])
            name = name.replace(word, mapping[word])
    return name

def test():
    st_types = audit()

    pprint.pprint(dict(st_types))
    unicodecount = 0
    for st_type, ways in st_types.items():  #v2 is iteritems()
        #print ways
        for name in ways:
            print name
            better_name = update_name(name, mapping)
            if isinstance(better_name, unicode):
                # print sys.stdout.encoding  # shows computer's unicode encoding is UTF-8
                better_name = unicode(better_name).encode('utf8')
                better_name = better_name.replace("\xe2\x80\x93", "-")
                unicodecount += 1
            print (name, "=>", better_name)
    print 'Number of Unicaode entries:', unicodecount
    
if __name__ == '__main__':
    test()
