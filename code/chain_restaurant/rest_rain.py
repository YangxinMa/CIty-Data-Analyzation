# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 23:44:33 2021

@author: admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins
import analize_city

#https://stackoverflow.com/questions/59857949/how-to-add-cluster-markers-to-choropleth-with-folium
#https://stackoverflow.com/questions/42756934/how-to-plot-lat-and-long-from-pandas-dataframe-on-folium-map-group-by-some-label#
#https://georgetsilva.github.io/posts/mapping-points-with-folium/
#my friend xiaotong teach me how to marker restaurants in different and recommend me many used website to create map.
def ColorPoint(df, map_osm):
    if df['name'] == 'McDonald':
        r = 'blue'
    elif df['name'] == 'White Spot':
        r = 'green'
    elif df['name'] == 'Tim Hortons':
        r = 'red'
    elif df['name'] == 'Starbucks':
        r = 'black'
    elif df['name'] == 'AW':
        r = 'orange'
    elif df['name'] == 'Subway':
        r = 'purple'
    folium.CircleMarker(
        [df['lat'], df['lon']],
        radius=1,
        color=r,
    ).add_to(map_osm)


def chainCluster(df, map_osm):
    folium.Marker(
    location=[df['lat'], df['lon']],
    icon=None
    ).add_to(map_osm)




def main():
    data = pd.read_json('amenities-vancouver.json.gz', lines=True)
    McDonand = data[data['name']=="McDonald's"]
    White_Spot = data[data['name']=="White Spot"]
    Tim_Hortons = data[data['name']=="Tim Hortons"]
    starB = data[data['name']=="Starbucks"]
    AW = data[data['name']=="AW"]
    Subway = data[data['name']=="Subway"]
    McDonand.replace("McDonald's", 'McDonald')
    chain_restaurants = [McDonand.replace("McDonald's", "McDonald"),White_Spot,Tim_Hortons,starB, AW, Subway]
    chain_restaurants = pd.concat(chain_restaurants)
    chain_restaurants=chain_restaurants[['lat', 'lon', 'tags', 'name']]
    localchain=chain_restaurants[['lat', 'lon', 'name']]
    Vancouver = [49.282730, -123.120735]

    m = folium.Map(location=Vancouver,zoom_start=12)
    localchain.apply(ColorPoint, axis=1,map_osm=m)
    #markerRest = plugins.MarkerCluster().add_to(m)
    #https://www.kite.com/python/answers/how-to-convert-a-pandas-dataframe-column-of-strings-to-floats-in-python
    m.save("ColorPoint.html")
    
    
    #show density of chain
    m = folium.Map(location=Vancouver ,zoom_start=12)
    marker_cluster = plugins.MarkerCluster().add_to(m)
    localchain.apply(chainCluster, axis=1, map_osm=marker_cluster)
    marker_cluster.save("ChainsCluster.html")
    
    #not chain
    data = pd.read_csv('bar.csv')
    data1 = pd.read_csv('bbq.csv')
    data2 = pd.read_csv('cafe.csv')
    data3 = pd.read_csv('ice.csv')
    data4 = pd.read_csv('fast_food.csv')
    data5 = pd.read_csv('restaurant.csv')
    Notchain_restaurants = [data,data1,data2,data3,data4,data5]
    Notchain_restaurants = pd.concat(Notchain_restaurants)
    NotChain= Notchain_restaurants[Notchain_restaurants['name']!="White Spot"]
    NotChain= NotChain[NotChain['name']!="McDonald's"]
    NotChain= NotChain[NotChain['name']!="Tim Hortons"]
    NotChain= NotChain[NotChain['name']!="Starbucks"]
    NotChain= NotChain[NotChain['name']!="AW"]
    NotChain= NotChain[NotChain['name']!="Subway"]
    m = folium.Map(location=Vancouver ,zoom_start=12)
    marker_cluster = plugins.MarkerCluster().add_to(m)
    NotChain.apply(chainCluster, axis=1, map_osm=marker_cluster)
    marker_cluster.save("NotChainsCluster.html")
    
    
    



if __name__ == '__main__':
    main()