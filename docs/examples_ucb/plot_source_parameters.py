"""
Corner plots
============

Produce corner plots for a single sources' parameters.
"""

#%% 
# Load catalog and select individual source
import os
import numpy as np
import pandas as pd
import lisacattools.lisacattools as lisacat

#load catalog
catFile = 'cat15728640_v2/cat15728640_v2.h5'
cat = pd.read_hdf(catFile, key='detections')

#parse catFile to get path to chain files
catPath = os.path.split(catFile)[0]

#get index of source with maximum SNR
sourceId = cat.index.values[np.argmin(np.abs(np.array(cat['SNR'])-cat['SNR'].max()))]
cat.loc[[sourceId],['SNR','Frequency']]

#%%
# Corner plot of select source parameters using `corner` module

import corner

#read in the chain samples for this source
samples = lisacat.getChain(cat,sourceId,catPath)

#list of subset of paramters that are particularly interesting
parameters = ['Frequency','Frequency Derivative','Amplitude','Inclination']

#corner plot of source. 
fig=corner.corner(samples[parameters])

#%%
# Can also be done with ChainConsumer for prettier plots
from chainconsumer import ChainConsumer

#get dataframe into numpy array (this shouldn't be necessary)
df = samples[parameters].values

#rescale columns
df[:,0] = df[:,0]*1000 #f in mHz
df[:,1] = df[:,1]/1e-15 #df/dt
df[:,2] = df[:,2]/1e-22 #A
df[:,3] = df[:,3]*180./np.pi #inc in deg
parameter_symbols = [r'$f\ {\rm [mHz]}$',
                     r'$\dot{f}\ [s^{-2}]\times 10^{-16}$',
                     r'$\mathcal{A} \times 10^{-23}$',
                     r'$\iota\ {\rm [deg]}$']

#add source chain to ChainConsumer object
c = ChainConsumer().add_chain(df,parameters=parameter_symbols,cloud=True)

#plot!
fig = c.plotter.plot(figsize=1.5)
