"""
Full catalog corner plots
=========================

Corner plot of select parameters for the full catalog.
"""

import glob
import numpy as np
import pandas as pd
import corner
import seaborn as sns
import matplotlib.pyplot as plt
import lisacattools.lisacattools as lisacat
from chainconsumer import ChainConsumer

#%%
# Load the catalog files

# Find the list of catalogs
catFiles = glob.glob('MBH_wk*C.h5')

# Read individual DataFrames' metadata by specifying the key parameter
dfs = list()
for catFile in catFiles:
    df = pd.read_hdf(catFile, key = 'metadata')
    df['location'] = catFile
    dfs.append(df) 
meta = pd.concat(dfs)

# sort metadata by observation week, putting most recent catalog last in the list
meta = meta.sort_values(by='observation week')

# load the detections 
catIdx = len(meta)-1
catName = meta.index[catIdx]
catFile = meta.iloc[catIdx]['location']
cat = pd.read_hdf(catFile, key='detections')

#%%
# Create the corner plot with ChainConsumer

c = ChainConsumer()

# selected parameters to plot
parameters = ['Mass 1','Mass 2', 'Luminosity Distance']

# how parameter names should be formatted in figure
parameter_symbols = [r'$m_1\ [{\rm M}_\odot]$',
                     r'$m_2\ [{\rm M}_\odot]$',
                     r'$D_L\ [{\rm Gpc}]$', 
                    ]

sources = list(cat.index)
for source in sources:

    # get chain samples
    samples = lisacat.getChain(cat,source)
    
    # get dataframe into numpy array
    df = samples[parameters].values
    
    # add samples to chainconsumer
    c.add_chain(df,parameters=parameter_symbols,name=source)
    
#plot!
c.configure(plot_hists=False)
fig = c.plotter.plot(figsize=1.5,log_scales=True)
