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


# In[3]:


def nearest_point(point, remain):
 
    d = []
    for i in range(len(remain)):
        d.append(math.dist(point,remain[i]))
    return d.index(min(d))
        

def shortest_path(coors):
    
    path = [coors[0]]
    remain = coors[1:len(coors)]

    
    for i in range(len(remain)):
        p = nearest_point(path[-1], remain)
        path.append(remain[p])
        remain.remove(remain[p])

    
    return path


# In[4]:


def get_routes(G_walk, coors):
    
    routes = []
    
    for i in range(len(coors) - 1):
        orig_node = ox.get_nearest_node(G_walk,
                                (coors[i][0], coors[i][1]))

        dest_node = ox.get_nearest_node(G_walk,
                                        (coors[i+1][0], coors[i+1][1]))

        route = nx.shortest_path(G_walk,
                                 orig_node,
                                 dest_node,
                                 weight='length')
        routes.append(route)
    return routes


# In[5]:


def random_color():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return "#" + color


# In[6]:


def routes_map(G_walk, routes):
    route_map = ox.plot_route_folium(G_walk, routes[0], color = random_color())
    if len(routes) == 1:
        return route_map
    for i in range(1,len(routes)):
        route_map = ox.plot_route_folium(G_walk, routes[i], route_map=route_map, color=random_color())
    return route_map


# In[ ]:





# In[7]:


def main():
    
    df = pd.read_csv('data/wiki_grade.csv')
    
    df['city'] = df.apply(analize_city.give_city_name, axis=1)
    
    #Reference: https://stackoverflow.com/questions/29791785/python-pandas-add-a-column-to-my-dataframe-that-counts-a-variable
    df['count'] = df.groupby('name')['name'].transform('count')
    
    df = df[df['amenity'] != 'fast_food']
    
    df_not_chain = df[df['count'] < 10]
    
    df_not_chain = df_not_chain[df_not_chain['city'] == 'Vancouver']
    
    famous = df_not_chain.groupby(['catagorities'], sort=False)['entry_len'].max()
    
    
    famous_food = df_not_chain[(df_not_chain['catagorities'] == 'food') & (df_not_chain['entry_len'] == famous.food)].to_numpy()[0]
    famous_food_loc = [famous_food[0], famous_food[1]]

    famous_service = df_not_chain[(df_not_chain['catagorities'] == 'service') & (df_not_chain['entry_len'] == famous.service)].to_numpy()[0]
    famous_service_loc = [famous_service[0], famous_service[1]]

    famous_medical = df_not_chain[(df_not_chain['catagorities'] == 'medical') & (df_not_chain['entry_len'] == famous.medical)].to_numpy()[0]
    famous_medical_loc = [famous_medical[0], famous_medical[1]]

    famous_facility = df_not_chain[(df_not_chain['catagorities'] == 'facility') & (df_not_chain['entry_len'] == famous.facility)].to_numpy()[0]
    famous_facility_loc = [famous_facility[0], famous_facility[1]]

    famous_education = df_not_chain[(df_not_chain['catagorities'] == 'education') & (df_not_chain['entry_len'] == famous.education)].to_numpy()[0]
    famous_education_loc = [famous_education[0], famous_education[1]]

    famous_transportation = df_not_chain[(df_not_chain['catagorities'] == 'transportation') & (df_not_chain['entry_len'] == famous.transportation)].to_numpy()[0]
    famous_transportation_loc = [famous_transportation[0], famous_transportation[1]]

    coors = [famous_food_loc, famous_service_loc, famous_medical_loc,famous_facility_loc, famous_education_loc, famous_transportation_loc]
    
    shortest_paths = shortest_path(coors)
    
    #Reference: https://stackoverflow.com/questions/60578408/is-it-possible-to-draw-paths-in-folium
    #I learned how to draw a path from this web,
    
    ox.config(log_console=True, use_cache=True)

    G_walk = ox.graph_from_place('Vancouver, British Columbia, Canada',
                                 network_type='walk')

    routes = get_routes(G_walk, shortest_paths)

    route_map = routes_map(G_walk,routes)

    route_map.save('html/route.html')


# In[8]:


if __name__=='__main__':
    main()


# In[ ]:




