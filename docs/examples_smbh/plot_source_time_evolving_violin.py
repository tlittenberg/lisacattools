"""
Time-evolving violin plot
=================================

Violin plot of select parameters for a single source showing how 
parameter estimation changes with observing time over all observing epochs
"""

import glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import lisacattools.lisacattools as lisacat

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

# For plotting purposes, we add a new parameter that is merger time error (in hours), expressed relative to median merger time after observation is complete
latestWeek = np.max(allEpochs['Observation Week'])
allEpochs['Merge Time Error'] = (allEpochs['Barycenter Merge Time']-np.median(allEpochs[allEpochs['Observation Week']==latestWeek]['Barycenter Merge Time']))/3600


#%%
# Create the violin plot

# select the parameters to plot and scaling (linear or log) for each
params = ['Mass 1','Mass 2','Spin 1','Spin 2','Luminosity Distance','Merge Time Error']
scales = ['log','log','linear','linear','linear','linear']

# arrange the plots into a grid of subplots
ncols = 2
nrows = np.int(np.ceil(len(params)/ncols))
fig = plt.figure(figsize=[10,10],dpi=100)

# plot the violin plot for each parameter
for idx,param in enumerate(params):
    ax = fig.add_subplot(nrows,ncols,idx+1)
    sns.violinplot(ax = ax, x='Observation Week', y=param, data=allEpochs,scale='width',width=0.8,inner='quartile')
    ax.set_yscale(scales[idx])
    ax.grid(axis='y')
    
# add an overall title    
fig.suptitle('Parameter Evolution for %s' % sourceIdx)






