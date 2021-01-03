"""
Source list
====================

Display a table of catalog files, detection list, and timeline of mergers..
"""

#%% 
# Load catalog and display list
import glob 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# get list catalog files
catFiles = glob.glob('MBH_wk*C.h5')

# append catalog files to master data frame
dfs = list()
for catFile in catFiles:
    df = pd.read_hdf(catFile, key = 'metadata')
    df['location'] = catFile
    dfs.append(df) 
meta  = pd.concat(dfs)
meta = meta.sort_values(by='observation week')

#%% 
# Load detections from final catalog. 
# Because catalogs are cummulative, this will include all sources

# select last catalog in list
catIdx = len(meta)-1
catFile = meta.iloc[catIdx]['location']
cat = pd.read_hdf(catFile, key='detections')
cat[['Log Likelihood','Mass 1','Mass 2','Luminosity Distance']]

#%%
# Cumulative plot of observed mergers

# sort events by merger time
cat.sort_values(by='Barycenter Merge Time',ascending=True, inplace=True)
mergeTimes = cat['Barycenter Merge Time']
mergeT = np.insert(np.array(mergeTimes)/86400,0,0)
mergeCount = np.arange(0,len(mergeTimes)+1)

# setup plot
fig, ax = plt.subplots(figsize = [8,6],dpi=100)

# configure axes
ax.step(mergeT,mergeCount,where='post')
ax.set_xlabel('Observation Time [days]')
ax.set_ylabel('Merger Count')
ax.grid()

# loop over events by merger time and make annotated figure
for m in range(0,len(mergeTimes)):
    plt.annotate(mergeTimes.index[m], # this is the text
                 (mergeTimes[m]/86400,mergeCount[m]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(2,5), # distance from text to points (x,y)
                ) 
plt.show()


