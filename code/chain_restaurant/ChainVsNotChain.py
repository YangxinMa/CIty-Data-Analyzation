# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 21:15:49 2021

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 23:44:33 2021

@author: admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import analize_city
from scipy.stats import mannwhitneyu
from scipy.stats import chi2_contingency


OUTPUT_TEMPLATE = (
    '"Are there some citites have more restaurant ?" p-value:  {more_rest:.3g}\n'
)


def main():
    data= pd.read_csv('wiki_grade.csv')

    #city of chain
    #this is my partner code which I can use directly.
    data['city'] = data.apply(analize_city.give_city_name, axis=1)
    data['count'] = data.groupby('name')['name'].transform('count')
    McDonand = data[data['name']=="McDonald's"]
    White_Spot = data[data['name']=="White Spot"]
    Tim_Hortons = data[data['name']=="Tim Hortons"]
    starB = data[data['name']=="Starbucks"]
    AW = data[data['name']=="AW"]
    Subway = data[data['name']=="Subway"]

    McDonand.replace("McDonald's", 'McDonald')
    chain_restaurants = [McDonand.replace("McDonald's", "McDonald"),White_Spot,Tim_Hortons,starB, AW, Subway]
    chain_restaurants = pd.concat(chain_restaurants)
    
    V = chain_restaurants[chain_restaurants['city']=='Vancouver']
    R = chain_restaurants[chain_restaurants['city']=='Richmond']
    S = chain_restaurants[chain_restaurants['city']=='Surrey']
    B =chain_restaurants[chain_restaurants['city']=='Burnaby']
    C = chain_restaurants[chain_restaurants['city']=='Coquitlam']
    NV = chain_restaurants[chain_restaurants['city']=='Not In Vancouver']
    Vlen=len(V)
    Rlen=len(R)
    Slen=len(S)
    Blen=len(B)
    Clen=len(C)
    NVlen=len(NV)

    
    plt.figure(figsize=(6, 6))
    label = ['Vancouver', 'Richmond', 'Surrey', 'Burnaby', 'Coquitlam', 'Not In Vancouver']
    explode = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    values = [V.iloc[:, 0].size, R.iloc[:, 0].size, S.iloc[:, 0].size,B.iloc[:, 0].size, C.iloc[:, 0].size, NV.iloc[:, 0].size]
    plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')
    plt.title('Chain restaurant in different cities')
    plt.savefig('Chain restaurant pie')
    
    NotChain= data[data['name']!="White Spot"]
    NotChain= NotChain[NotChain['name']!="McDonald's"]
    NotChain= NotChain[NotChain['name']!="Tim Hortons"]
    NotChain= NotChain[NotChain['name']!="Starbucks"]
    NotChain= NotChain[NotChain['name']!="AW"]
    NotChain= NotChain[NotChain['name']!="Subway"]
    
    V = NotChain[NotChain['city']=='Vancouver']
    R = NotChain[NotChain['city']=='Richmond']
    S = NotChain[NotChain['city']=='Surrey']
    B =NotChain[NotChain['city']=='Burnaby']
    C = NotChain[NotChain['city']=='Coquitlam']
    NV = NotChain[NotChain['city']=='Not In Vancouver']
    Vlen2=len(V)
    Rlen2=len(R)
    Slen2=len(S)
    Blen2=len(B)
    Clen2=len(C)
    NVlen2=len(NV)
    
    plt.figure(figsize=(6, 6))
    label = ['Vancouver', 'Richmond', 'Surrey', 'Burnaby', 'Coquitlam', 'Not In Vancouver']
    explode = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    values = [V.iloc[:, 0].size, R.iloc[:, 0].size, S.iloc[:, 0].size,B.iloc[:, 0].size, C.iloc[:, 0].size, NV.iloc[:, 0].size]
    plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')
    plt.title('Not Chain restaurant in different cities')
    plt.savefig('Not Chain restaurant pie')
    
    #chi test of restaurants in different cities
    obs=[[Vlen,Rlen,Slen,Blen,Clen,NVlen],[Vlen2,Rlen2,Slen2,Blen2,Clen2,NVlen2]]
    chi, p, dof, ex = chi2_contingency(obs)
    
        


    print(OUTPUT_TEMPLATE.format(
        more_rest=p,

    ))


   

    #display(chain_restaurants)
    
    
    



if __name__ == '__main__':
    main()