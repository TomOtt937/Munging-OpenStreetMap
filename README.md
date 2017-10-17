## Description
This data wrangling project was completed for the Udacity.com Data Analyst Nanodegree and uses data munging techniques to clean a dataset from OpenStreetMap.org.  Python 2.7 is used to initially examine the OSM dataset, find and clean issues within the data, then writing the data to a CSV format that can be imported into a SQL database.  SQLite is then used to further explore and clean the data.  The wrangling process was developed using the Jupyter Notebook environment.

## Documents
* CentervilleArea2.osm – OpenStreetMap dataset used for testing.
  * Data pulled from http://overpass-api.de/query_form.html using bounds
    * minlat: 39.5861000
    * maxlon: -84.0799000
    * minlon: -84.1905000
    * maxlat: 39.6754000

* OpenStreetMap Project - Ott.pdf – This file documents the data wrangling process and was knitted from Jupyter Notebook.

* References.txt – This text file contains a list of references used while completing the project.

* SQL Schema.txt – A list of commands used in SQLite3 to create the tables.

Python code moved from Notebook to the following scripts:

* script-DisplayBounds.py – This script was the first cell in Notebook to load the desired file for processing.  Starting with this script allowed for easy change between machines, and between the test dataset and the full dataset.

* script-DisplayStreetTypes.py – This script creates a list of street types in the dataset along with a count of each.

* script-UpdateStreetTypes.py – This script was used to further explore street types and develop the code that was used to correct the street type abbreviations.  This is also where I discovered the Unicode entries and how to convert these entries into string format.

* script-DisplayTagList.py – This script displays a list of the tags used in node entries vs. way entries.  It also shows a count of node and way entries with no tags that was used to validate a SQL statement.  Unicode to String conversion is further developed in this script.

* script-ZipCodeAudit.py – This script displays a list of zip codes along with a count of each.  Can print a list of questionable zip codes.  Note that the troubled zip codes are in the full dataset; there are none in the example dataset.

* script-DisplayEntry.py – This script displays a whole node or way entry (including tags/nodes) for a given ID.

* script-StoreData.py - This is the scrip used to clean the OpenStreetMap dataset and store it in .csv files for SQL import.
