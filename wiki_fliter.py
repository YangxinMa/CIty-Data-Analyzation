#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import folium
import osmnx as ox
import networkx as nx
#Reference:https://pypi.org/project/Wikidata/
#wiki API
from wikidata.client import Client


# In[6]:


df = pd.read_json('amenities-vancouver.json.gz', lines=True)


# In[17]:


def check_wiki(x):
    if 'brand:wikidata' in x:
        return True
    return False

def entry_num(x):
    return x['brand:wikidata']

def entry_len(x,client):
    entity = client.get(x, load=True)
    return len(entity)

client = Client()

df['wiki'] = df['tags'].apply(check_wiki)

df_wiki = df[df['wiki'] == True]

df_wiki.loc[:,'entry_num'] = df_wiki['tags'].apply(entry_num)

food = ['cafe', 'fast_food', 'bbq', 'restaurant', 'pub', 'bar', 'food_court', 'ice_cream', 'bistro', 'juice_bar', 
        'disused:restaurant', 'water_point', 'biergarten']

facility = ['drinking_water','shelter', 'bench', 'atm', 'luggage_locker', 'lobby', 'lounge', 'vending_machine', 
            'post_box', 'telephone', 'waste_basket', 'recycling', 'fountain', 'waste_disposal', 'social_facility', 
            'clock', 'toilets', 'shower','family_centre', 'playground', 'smoking_area', 'trash', 'leisure', 
            'letter_box','Observation Platform']

service = ['bureau_de_change','marketplace', 'storage', 'money_transfer', 'shop|clothes','community_centre', 
           'post_office', 'bank', 'photo_booth', 'construction', 'post_depot', 'conference_centre', 'fire_station', 
           'police', 'compressed_air', 'townhall', 'scrapyard', 'courthouse', 'events_venue', 'ATLAS_clean_room', 
           'workshop', 'safety', 'animal_shelter', 'internet_cafe', 'social_centre', 'vacuum_cleaner', 'studio', 
           'ranger_station', 'storage_rental', 'sanitary_dump_station', 'housing co-op', 'loading_dock', 'monastery', 
           'gym', 'payment_terminal', 'atm;bank', 'waste_transfer_station', 'office|financial']

education = ['childcare', 'school', 'university', 'library','public_bookcase', 'college', 'kindergarten',
             'music_school','language_school', 'prep_school', 'cram_school', 'science', 'driving_school',
            'training', 'research_institute']

medical = ['pharmacy', 'dentist', 'doctors', 'clinic', 'veterinary', 'nursery', 'hospital', 'meditation_centre',
          'healthcare', 'first_aid', 'chiropractor', 'Pharmacy']

entertament = ['place_of_worship', 'public_building', 'cinema', 'theatre', 'dojo', 'arts_centre', 'nightclub', 
               'stripclub','gambling', 'spa', 'watering_place', 'park', 'casino', 'hunting_stand']

transportation = ['car_sharing', 'parking_entrance', 'fuel', 'ferry_terminal', 'car_rental','seaplane terminal', 
                  'charging_station', 'taxi', 'EVSE','car_rep', 'motorcycle_rental', 'bus_station','boat_rental', 
                  'motorcycle_rental', 'bus_station', 'boat_rental''parking_entrance', 'bicycle_parking', 'parking',
                  'bicycle_rental', 'car_wash', 'bicycle_repair_station','parking_space', 'trolley_bay', 
                  'motorcycle_parking','boat_rental', 'motorcycle_rental']


def set_catagorities(x):
    if x in food:
        return 'food'
    if x in facility:
        return 'facility'
    if x in service:
        return 'service'
    if x in education:
        return 'education'
    if x in medical:
        return 'medical'
    if x in entertament:
        return 'entertament'
    if x in transportation:
        return 'transportation'
    return 'other'

df_wiki.loc[:,'catagorities'] = df_wiki['amenity'].apply(set_catagorities)

df_wiki.loc[:,'entry_len'] = np.vectorize(entry_len)(df_wiki['entry_num'], client)

df_wiki.to_csv('data/wiki_grades.csv',index = False)

