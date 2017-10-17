'''
Display all of the tag types with a count of each.  
Display all of the key types for Node tags and for Way tags.
How many Node and Way entries have no additional info in tag entries?
Conversion Unicode to String.
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

def check_for_unicode(tag):
    if isinstance(tag.attrib['k'], unicode):
        print tag
    if isinstance(tag.attrib['v'], unicode):
        ''' uncommenting the print commands in this sub-routine results in a lot of output;
                used to identify unicode characters for conversion to string '''
        #print tag.attrib
        tag.attrib['v'] = unicode(tag.attrib['v']).encode('utf8')
        tag.attrib['v'] = tag.attrib['v'].replace("\xe2\x80\x93", '-')
        tag.attrib['v'] = tag.attrib['v'].replace("\xe2\x80\x99", "'")
        tag.attrib['v'] = tag.attrib['v'].replace("\xe2\x80\x9c", '"')
        tag.attrib['v'] = tag.attrib['v'].replace("\xe2\x80\x9d", '"')
        tag.attrib['v'] = tag.attrib['v'].replace("\xc2\xae", '')
        tag.attrib['v'] = tag.attrib['v'].replace("\xc3\xa4", 'a')
        #print tag.attrib
        #print

def count_tags():
    osm_file = open(datafile, "r")
    mainTags = {}
    nodeTags = {}
    wayTags = {}
    nodeTagKeys = {}
    wayTagKeys = {}

    
    countNodes = 0
    countWays = 0
    zeroNodeTags = 0
    zeroWayTags = 0
    countNodeTags = 0
    countWayTags = 0
    elementcount = 0   
    tagCount = 0 
    idhold = ''
    
    for event, elem in ET.iterparse(osm_file):
        elementcount += 1
        if elem.tag not in mainTags:
            mainTags[elem.tag] = 1
        else:
            mainTags[elem.tag] += 1
            
        tagCount = 0
        for tag in iter(elem):
            if tag.tag == 'tag':
                tagCount =+ 1
            if elem.tag == 'node':
                #countNodeTags += 1
                idhold = elem.attrib['id']
                if tag.tag not in nodeTags:
                    nodeTags[tag.tag] = 1
                else:
                    nodeTags[tag.tag] += 1
                if tag.tag == 'tag':
                    #print tag.tag, tag.attrib, tag.attrib['k']
                    if tag.attrib['k'] not in nodeTagKeys:
                        nodeTagKeys[tag.attrib['k']] = 1
                    else:
                        nodeTagKeys[tag.attrib['k']] += 1
            elif elem.tag == 'way':
                idhold = elem.attrib['id']
                if tag.tag not in wayTags:
                    wayTags[tag.tag] = 1
                else:
                    wayTags[tag.tag] += 1
                if tag.tag == 'tag':
                    if tag.attrib['k'] not in wayTagKeys:
                        wayTagKeys[tag.attrib['k']] = 1
                    else:
                        wayTagKeys[tag.attrib['k']] += 1
            ''' code to see the values of a less common key '''
            #if tag.tag == 'tag' and elem.tag in ['node', 'way']:
            #        if tag.attrib['k'] == 'type':
            #            print elem.tag, idhold, tag.attrib['k'], tag.attrib['v']

            if tag.tag == 'tag' and elem.tag in ['node', 'way']:
                check_for_unicode(tag)

            
        if elem.tag == 'node':
            countNodes += 1
            if tagCount == 0:
                zeroNodeTags += 1
        elif elem.tag == 'way':
            countWays += 1
            if tagCount == 0:
                zeroWayTags += 1

        ''' code to limit the run for testing '''
        #if elementcount == 100:
        #    break

    # Show a count of nodes and ways with no tag entries for validation agains SQL counts
    print 'Nodes with no tags:', zeroNodeTags, 'of', countNodes, str("%.2f%%" % (100. * zeroNodeTags / countNodes))
    print 'Ways with no tags:', zeroWayTags, 'of', countWays, str("%.2f%%" % (100. * zeroWayTags / countWays))
    return mainTags, nodeTags, wayTags, nodeTagKeys, wayTagKeys

def test():
    mainTags, nodeTags, wayTags, nodeTagKeys, wayTagKeys = count_tags()
    print '---', len(mainTags), 'Main Tags ---'
    pprint.pprint(mainTags)
    print '---', len(nodeTags), 'Node Tags ---'
    pprint.pprint(nodeTags)
    print '---', len(nodeTagKeys), 'Node Tag Keys ---'
    pprint.pprint(nodeTagKeys)    
    print '---', len(wayTags), 'Way Tags ---'
    pprint.pprint(wayTags)
    print '---', len(wayTagKeys), 'Way Tag Keys ---'
    pprint.pprint(wayTagKeys)    
    
#count_tags()
if __name__ == "__main__":
    test()
