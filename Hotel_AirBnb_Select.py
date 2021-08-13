#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import folium
import osmnx as ox
import networkx as nx
#Reference:https://pypi.org/project/Wikidata/
#wiki API
from wikidata.client import Client
import math
import copy
from geopy.geocoders import Nominatim
from folium import plugins
import trip_trail
import analize_city
import random
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from collections import Counter


# In[4]:


def main():
    df = pd.read_csv('wiki_grades.csv')
    df = df[df['amenity'] == 'restaurant']
    df['city'] = df.apply(analize_city.give_city_name, axis=1)
    df = df[df['city'] == 'Vancouver']
    coors = list(df[['lat','lon']].itertuples(index=False, name=None))
    
    #Data standardization
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(coors)
    
    
    #Reference:https://realpython.com/k-means-clustering-python/
    #I learned how to use kmean form this web
    
    #Find the appropriate number of clusters

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
        }
    
    #let k from 1 to 11, get the sum of squared errors for each k
    sse = []

    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)
    
    #Use elbow method to find the appropriate k
    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )
    k = kl.elbow
    
    
    #After we find the appropriate k value, use it to train the kmeans model
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    
    #Now we got k center point. Because we did the data standardization,
    #we need to inverse the data standardization. 
    #We need the real location point to plot on the map
    centers = kmeans.cluster_centers_
    centers = scaler.inverse_transform(centers)
    centers = centers.tolist()
    
    #We recommand clients choose hotel around the largest clusters center point.
    #Find the index for largest cluster center point
    recommand = list(Counter(kmeans.labels_))[0]
    
    #Create the map
    Vancouver = [49.282730, -123.120735]
    vmap = folium.Map(location=Vancouver, tiles='OpenStreetMap', zoom_start=12)
    
    #All restaurants location points. 
    for point in range(0, len(coors)):
        folium.Marker(coors[point],icon=folium.Icon(color='blue')).add_to(vmap)
    vmap.save("restaurants_vancouver.html")
    
    #All center location points.The black one is the best one. 
    for point in range(0, len(centers)):
        if point == recommand:
            folium.Marker(centers[point],icon=folium.Icon(color='black')).add_to(vmap)
        else:
            folium.Marker(centers[point],icon=folium.Icon(color='red')).add_to(vmap)

    vmap.save("Hotel_AirBnb_Select.html")


# In[5]:


if __name__=='__main__':
    main()


# In[ ]:




