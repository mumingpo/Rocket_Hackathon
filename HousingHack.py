#!/usr/bin/env python
# coding: utf-8

# In[247]:


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


# In[275]:


def fetch_housing_data():
    return pd.read_csv(r"converted_rent_only.csv", 'r')





# In[274]:


def filter(housingData):
    
    housingData = housingData[housingData["SERIALNO"].notnull()]
    housingData = housingData[housingData["PUMA"].notnull()]
    housingData = housingData[housingData["NP"].notnull()]
    housingData = housingData[housingData["R18"].notnull()]
    housingData = housingData[housingData["R60"].notnull()]
    housingData = housingData[housingData["R65"].notnull()]
    housingData = housingData[housingData["NOC"].notnull()]
    housingData = housingData[housingData["RNTP"].notnull()]
    housingData = housingData[housingData["FINCP"].notnull()]
    
    invalid_rows = (12 * housingData["RNTP"] - 0.5 * housingData["FINCP"] < 0)
    housingData = housingData[-invalid_rows]
    return housingData;


# In[271]:


def getDeficit(rent, income) :
    tot = rent - (.5*income)
    if(tot < 0):
        return 0
    return tot


# In[272]:


def calcWeights(weights, persons, children, R18, R60, R65):
    ct = sum(1 for row in housingData)
    for i in range(ct):
        weights[i] = persons[i] + 1.3*children[i] + 1.1*R18[i] + R60[i] + R65[i] + 0.1*np.random.rand()
    return weights
    


# In[273]:


def calcExpanditure(weights, M, deducts):
    ct = sum(1 for row in housingData)
    expanditure = [0]*ct
    weightsPr, inds = zip(*sorted([(j, i) for i, j in enumerate(weights)]))
    for i in range(ct):
        if deducts[inds[i]] >= M:
            expanditure[inds[i]] = M
        else:
            expanditure[inds[i]] = deducts[inds[i]]
        M = M - expanditure[inds[i]]
    return expanditure


# In[301]:


def init():
    housingData = fetch_housing_data()
    housingData = filter(housingData)
    ct = sum(1 for row in housingData)
    rents = []
    incomes = []
    persons = []
    children = []
    R18 = []
    R60 = []
    R65 = []
    areas = []
    deducts = []
    weights = [0]*ct
    expenditures = [0]*ct
    M = 50000000
    for i in range(ct):
        areas.append(housingData["PUMA"].iloc[i])
    for i in range(ct):
        rents.append(12 * housingData["RNTP"].iloc[i])
    for i in range(ct):
        incomes.append(housingData["FINCP"].iloc[i])
    for i in range(ct):
        persons.append(housingData["NP"].iloc[i])
    for i in range(ct):
        children.append(housingData["NOC"].iloc[i])
    for i in range(ct):
        R18.append(housingData["R18"].iloc[i])
    for i in range(ct):
        R60.append(housingData["R60"].iloc[i])
    for i in range(ct):
        R65.append(housingData["R65"].iloc[i])
    for i in range(ct):
        deducts.append(getDeficit(rents[i], incomes[i]))
    weights = calcWeights(weights, persons, children, R18, R60, R65)
    expanditures = calcExpanditure(weights, M, deducts)
    
    expanditure_by_area = {3301:0., 3302:0., 3303:0., 3304:0., 3305:0., 3306:0., 3400:0.}
    for i, j in zip(areas, expanditures):
        expanditure_by_area[i] += j
    
    print(expanditure_by_area)
    
    legend = expanditure_by_area.keys()
    x = np.arange(len(legend))
    y = expanditure_by_area.values()
    plt.bar(x, y)
    plt.xticks(x, ["0{}".format(i) for i in legend])
    plt.show()


# In[302]:


init()


# In[ ]:



    


# In[ ]:




