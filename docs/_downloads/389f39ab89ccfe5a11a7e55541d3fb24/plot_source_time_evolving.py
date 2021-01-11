"""
Time-evolving parameter estimation
=================================

Corner plot of select parameters for a single source showing how 
parameter estimation changes with observing time.
"""

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lisacattools.lisacattools as lisacat
from chainconsumer import ChainConsumer


# Find the list of catalogs
catPath = 'MBH_catalog'
catFiles = glob.glob(catPath+'/MBH_wk*C.h5')

# Read individual DataFrames' metadata by specifying the key parameter
dfs = list()
for catFile in catFiles:
    df = pd.read_hdf(catFile, key = 'metadata')
    df['location'] = catFile
    dfs.append(df) 
meta = pd.concat(dfs)

# sort metadata by observation week, putting most recent catalog last in the list
meta = meta.sort_values(by='observation week')

# load and display the detections, sorted by primary mass 
catIdx = len(meta)-1
catName = meta.index[catIdx]
catFile = meta.iloc[catIdx]['location']
cat = pd.read_hdf(catFile, key='detections')
cat = cat.sort_values(by='Mass 1')
cat[['Parent','Log Likelihood','Mass 1', 'Mass 2', 'Luminosity Distance']]

#%% 
# Choose a source from the list of detections and get its history through the different catalogs

# Pick a source, any source
sourceIdx = 'MBH005546845'

# Get source history and display table with parameters and observing weeks containing source
srcHist = lisacat.getLineage(meta,catName,sourceIdx)
srcHist.drop_duplicates(subset='Log Likelihood',keep='last',inplace=True)
srcHist.sort_values(by='Observation Week',ascending=True,inplace=True)
srcHist[['Observation Week','Parent','Log Likelihood','Mass 1', 'Mass 2', 'Luminosity Distance']]

#%%
# Load chains for different observing epochs of selected source
epochs = list(srcHist.index)
dfs = list()
for epoch in epochs:
    df = lisacat.getChain(srcHist,epoch,catPath)
    df.insert(len(df.columns),'Source',epoch,True)
    df.insert(len(df.columns),'Observation Week',srcHist.loc[epoch]['Observation Week'],True)
    dfs.append(df[['Source','Observation Week','Mass 1','Mass 2','Spin 1','Spin 2','Ecliptic Latitude','Ecliptic Longitude','Luminosity Distance','Barycenter Merge Time','Merger Phase','Polarization', 'cos inclination']])

allEpochs = pd.concat(dfs)

#%%
# Create corner for multiple observing epochs

# Choose weeks for plot from source history table
wks = [4,8,10]

# select subset of parameters to plot
parameters = ['Mass 1','Mass 2','Luminosity Distance']
parameter_labels = [r'$m_1\ [{\rm M}_\odot]$',
                    r'$m_2\ [{\rm M}_\odot]$',
                    r'$D_L\ [{\rm Gpc}]$',
                   ]
ranges=[(10000,50000),
        (1000,5000),
        (16,40)]

c = ChainConsumer()
for idx,wk in enumerate(wks):
    epoch = allEpochs[allEpochs['Observation Week']==wk]
    samples = epoch[parameters].values

    c.add_chain(samples,parameters=parameter_labels,name='Week '+str(wk))

c.configure(cmap="plasma")
fig = c.plotter.plot(figsize=1.5, log_scales=False, extents=ranges)






