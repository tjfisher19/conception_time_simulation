# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:16:08 2021

@author: fishert4 and baileraj

A python program to simulate the number of months
until a couple conceived a child with the following 
assumptions:
    1. about 10% of couples will have fertility issues
       (assumed impact:  prob of conception replaced by 0.85*prob_conception)
    2. Prob of conception reduces each month slightly, 0.99*prob_conception,
       essentially this is an aging effect
    3. after 12 unsuccessful months, a couple will consult a fertility
       specialist, this will increase the conception probability by 15%
    4. After 24 months, the couple will stop trying

"""

#%%
import random as rd

def conception_simulation(alpha=1, beta=1):
    ## Generate a probability of conception for the couple
    prob_conception = rd.betavariate(alpha=alpha, beta=beta)

    ## Does the couple have fertility issues? 
    if rd.uniform(0,1) <= 0.1:
        prob_conception = prob_conception*0.85
    
    ## random.choices is similar to sample() in R
    ##  but returns list of size k elements
    ## We are only return 1, so we want to access preg[0]
    preg = rd.choices(("Pregnant", "Not"), weights=(prob_conception, 1-prob_conception),k=1)
    mon = 1       ## takes at least one month
    
    ## Some status indicators
    consult = 0
    stop = 0
    while(preg[0]=="Not" and stop==0):
        mon = mon + 1
        
        ## Aging effect
        prob_conception = prob_conception*0.99
        preg = rd.choices(("Pregnant", "Not"), weights=(prob_conception, 1-prob_conception),k=1)
    
        ## Check the status
        ##   12 months and still not pregnant? Seek help
        ##   24 months and still not pregnant, sop the process
        if(mon==12 and preg[0]=="Not"):  ## tried 12 months and not pregnant
            consult = 1
            prob_conception = 1.15*prob_conception
        if(mon==24 and preg[0]=="Not"):
            stop = 1
            mon = None
    return [mon, prob_conception, consult, stop]

#%%
out = []
mons = []
for i in range(1000):
    out.append(conception_simulation(alpha=2, beta=6) )
    mons.append(out[i][0])

#%%

import numpy as np

np.mean(mons)

## By default, numpy does not handle missing values well

import pandas as pd

mons_data = pd.Series(mons)

np.mean(mons_data)
np.nanmean(mons_data)
np.sum(mons_data.isnull())

np.std(mons_data)
np.median(mons_data)
np.nanmedian(mons_data)

import matplotlib.pyplot as plt

plt.hist(mons_data)




preg = []
x = 0
for i in range(100000):
    preg.append(rd.choices(("Pregnant", "Not"), weights=(0.3, 0.7), k=1))
    if(preg[i][0]=="Not"):
        x = x + 1

    