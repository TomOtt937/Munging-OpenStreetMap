'''
Display a list of zip codes with a count of how often used.
Can also display the id's of nodes and ways with questionable zip codes.
'''
import os
import xml.etree.cElementTree as ET
import pprint

#Update DATADIR and FILENAME as needed
DATADIR = "C:\\Users\\Home\\Documents\\TOM\\Udacity\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
#DATADIR = "C:\\Users\\Thomas\\Documents\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
FILENAME = "CentervilleArea2.osm"  #  12,340K
#FILENAME = "DaytonMetro2.osm"      # 110,026K

datafile = os.path.join(DATADIR, FILENAME) 

"""
Display a list of zip codes with a count of how often used.
Code adapted from Udacity lesson.
"""

def get_zip(element):
    for tag in element.iter():
        if tag.tag == 'tag':
            #print element.attrib
            if tag.attrib['k'] == 'addr:postcode':
                return tag.attrib['v']


def process_map():
    osm_file = open(datafile, "r")  
    zipcodes = {}
    for _, element in ET.iterparse(osm_file):
        if element.tag in ['node', 'way']:
            holdid = element.attrib['id']
            holdtag = element.tag
            zipcode = get_zip(element)
            if zipcode != None:
                if zipcode not in zipcodes:
                    zipcodes[zipcode] = 1
                else:
                    zipcodes[zipcode] += 1
                # display a list of entries with questionable zip codes
                if zipcode in ['45242', '85201', '4404']:
                    print holdtag, zipcode, holdid
    osm_file.close()
    return zipcodes

def test():

    zipcodes = process_map()
    print len(zipcodes), 'zipcodes'
    pprint.pprint(zipcodes)

if __name__ == "__main__":
    test()
