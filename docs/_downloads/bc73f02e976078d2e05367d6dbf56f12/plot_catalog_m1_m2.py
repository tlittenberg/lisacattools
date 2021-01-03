"""
Catalog mass plot
=================

Plot component masses of all detections
"""

import glob 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lisacattools.lisacattools as lisacat

# get list catalog files
catFiles = glob.glob('MBH_wk*C.h5')

# append catalog files to master data frame
dfs = list()
for catFile in catFiles:
    df = pd.read_hdf(catFile, key = 'metadata')
    df['location'] = catFile
    dfs.append(df) 
meta = pd.concat(dfs).sort_values(by='observation week')

# load the final list of detections 
catIdx = len(meta)-1
catFile = meta.iloc[catIdx]['location']
cat = pd.read_hdf(catFile, key='detections')


# plot the catalog in the m1-m2 plane
fig, ax = plt.subplots(figsize = [8,6],dpi=100)
srcs = list(cat.index)
for idx, src in enumerate(srcs):
    chain = lisacat.getChain(cat,src)
    l1,m1,h1 = np.quantile(np.array(chain['Mass 1']),[0.05,0.5,0.95])
    l2,m2,h2 = np.quantile(np.array(chain['Mass 2']),[0.05,0.5,0.95])
    if idx < 10:
        mkr = 'o'
    else:
        mkr = '^'
        
    ax.errorbar(m1,m2,xerr = np.vstack((m1-l1,h1-m1)),yerr = np.vstack((m2-l2,h2-m2)),label=src,markersize=6,capsize=2,marker=mkr,markerfacecolor='none')
ax.set_xscale('log', nonposx='clip')
ax.set_yscale('log', nonposy='clip')
ax.grid()
ax.set_xlabel('Mass 1 [MSun]')
ax.set_ylabel('Mass 2 [MSun]')
ax.legend(loc = 'lower right')

plt.show()
