Project Topic: OSM, Photos, and Tours

Team member:  Xiaohang Hu, Yangxin Ma, Xubin Wang

Libraries:
import sys
import pandas as pd
import os
from PIL import Image                  # using pip install PIL
from PIL.ExifTags import TAGS, GPSTAGS
import folium                          # using pip install folium
import copy
from geopy.geocoders import Nominatim  #using pip install geopy
from folium import plugins
1. read EXIF data from images
	Run python3 read_pic.py pics/
    