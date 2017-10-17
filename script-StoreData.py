import os
import xml.etree.cElementTree as ET
import pprint
import re
import csv
import codecs
import cerberus
import schema

# Code specific to Windows environment using Python 2.7.12.
# Developed in Jupyter Notebook and copied into a .py script.

# Identify where the input file resides on the local machine.
DATADIR = "C:\\Users\\Home\\Documents\\TOM\\Udacity\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
#DATADIR = "C:\\Users\\Thomas\\Documents\\Data Analyst Nanodegree\\4 - Data Wrangling\\Project"
FILENAME = "CentervilleArea2.osm"  #  12,340K - test file
#FILENAME = "DaytonMetro2.osm"      # 110,026K - full version
datafile = os.path.join(DATADIR, FILENAME)

# Display the bounds of the map
osm_file = open(datafile, "r")
for event, elem in ET.iterparse(osm_file):
    if elem.tag == 'bounds':
        print elem.tag
        for attribute in elem.attrib:
            print '%s: %s' %(attribute, elem.attrib[attribute])
        break

# Code reused from the Udacity lesson.
# %load schema.py
# Note: The schema is stored in a .py file in order to take advantage of the
# int() and float() type coercion functions. Otherwise it could easily stored as
# as JSON or another serialized format.

schema = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'integer', 'coerce': int},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}

'''
Much of this code is reused from the Udacity lesson
'''

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

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

def update_name(name, mapping):
    '''Updates street name abreviations (from do_tag section)'''
    for word in name.split(" "):
        if word in mapping:
            name = name.replace(word, mapping[word])
    return name

def unicode2string(value):
    '''converts unicode to string format (from do_tag section)'''
    value = unicode(value).encode('utf8')
    value = value.replace("\xe2\x80\x93", '-')
    value = value.replace("\xe2\x80\x99", "'")
    value = value.replace("\xe2\x80\x9c", '"')
    value = value.replace("\xe2\x80\x9d", '"')
    value = value.replace("\xc2\xae", '')
    value = value.replace("\xc3\xa4", 'a')
    return value

def do_tag(tag, node_attribs):
    '''this section shapes tag entires for storage'''
    for attribute in tag.attrib:
        temp_dict = {}
        temp_dict['id'] = node_attribs['id']
        
        pc = PROBLEMCHARS.search(tag.attrib['k'])
        if pc:
            continue
        lcc = LOWER_COLON.search(tag.attrib['k'])
        if lcc:
            temp_dict['type'], temp_dict['key'] = tag.attrib['k'].split(":", 1)                       
            temp_dict['value'] = tag.attrib['v']
        else:
            temp_dict['key'] = tag.attrib['k']
            temp_dict['type'] = 'regular'
            temp_dict['value'] = tag.attrib['v']
        
        # check for issues and correct
        #1 Street name issues (type abbreviations)
        if temp_dict['key'] == 'addr:street':
            temp_dict['value'] = update_name(temp_dict['value'], mapping)
        #2 convert unicode to string
        if isinstance(temp_dict['value'], unicode):
            temp_dict['value'] = unicode2string(temp_dict['value'])
        #3 Zip code issue (4 digit)
        if temp_dict['key'] == 'addr:postcode' and temp_dict['value'] == '4404':
            temp_dict['value'] = '45404'
            
        return temp_dict

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        for tag in element.iter():
            if tag.tag == 'node':
                for attribute in tag.attrib:
                    if attribute in NODE_FIELDS:
                        node_attribs[attribute] = tag.attrib[attribute]
            elif tag.tag == 'tag':
                tags.append(do_tag(tag, node_attribs))
    elif element.tag == 'way':
        position = 0
        for tag in element.iter():
            if tag.tag == 'way':
                for attribute in tag.attrib:
                    if attribute in WAY_FIELDS:
                        way_attribs[attribute] = tag.attrib[attribute]
            elif tag.tag == 'tag':
                tags.append(do_tag(tag, way_attribs))
            elif tag.tag == 'nd':
                temp_nd = {}
                temp_nd['id'] = way_attribs['id']
                temp_nd['node_id'] = tag.attrib['ref']
                temp_nd['position'] = position
                position += 1                
                way_nodes.append(temp_nd)

    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(validate):
    """Iteratively process each XML element and write to csv(s)"""
    osm_file = open(datafile, "r")
    
    with codecs.open(NODES_PATH, 'w') as nodes_file, \
        codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
        codecs.open(WAYS_PATH, 'w') as ways_file, \
        codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
        codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)
        
        '''Headers are not needed since the csv files are imported into already created tables'''
        #nodes_writer.writeheader()
        #node_tags_writer.writeheader()
        #ways_writer.writeheader()
        #way_nodes_writer.writeheader()
        #way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(osm_file, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

    osm_file.close()

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(validate=True)

