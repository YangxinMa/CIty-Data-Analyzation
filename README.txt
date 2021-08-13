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
from folium.plugins import MarkerCluster
import seaborn
import numpy as np
import osmnx as ox
import networkx as nx
from wikidata.client import Client
import math
import random
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from collections import Counter

Work Done By Xubin Wang: Get Photos, Form Trip Route and City Analyze
1. Read EXIF data from images
	Run python3 read_pic.py 
2. Draw route of your walk and find food and entertaments around
    Run python3 trip_trail.py
3. Analize data of Cities
    Run python3 analize_city.py
Work Done By Yangxin Ma:
1. Data fliter:
    Run python3 wiki_fliter.py
2. Provide a tour path of a city
    Run python3 tour_plan.py
3. Find a good hotel/AirBnb location
    Run python3 Hotel_AirBnb_Select.py

Work Done By Xiaohang Hu:
1. Marked chain restauratnts in different color in map.
   Run python3 rest_rain.py
2. Cluster chain restauratnts and not chain restauratnt in map.
   Run python3 rest_rain.py
3. Create Pie graph to show percentage of chain restauratnts and not chain restauratnt in different cities.
   Run python3 ChainVsNotChain.py
4. using chi2_test to get pvalue to show whether some place has more restauratnts.
   Run python3 ChainVsNotChain.py
   
    
