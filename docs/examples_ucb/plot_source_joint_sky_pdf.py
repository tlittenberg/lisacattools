"""
Joint PDF of sky location
=========================

Plot joint posterior of all catalog sources in galactic coordinates.
"""

#%%
# Load catalogs and combine chain samples
import os
import pandas as pd
import numpy as np  
import healpy as hp
from astropy.coordinates import SkyCoord
from astropy import units as u
import ligo.skymap.plot
import matplotlib.pyplot as plt
import lisacattools.lisacattools as lisacat

# Start by loading the main catalog file processed from GBMCMC outputs
catFile = 'cat15728640_v2/cat15728640_v2.h5'
catPath = os.path.split(catFile)[0]
cat = pd.read_hdf(catFile, key='detections')

# loop over all sources in catalog and append chain samples to new dataframe
sources = list(cat.index)
samples_list = list()
for source in sources:
    
    # get chain samples
    samples = lisacat.getChain(cat,source,catPath)

    # convert from ecliptic to galactic coordinates
    lisacat.getGalcoord(samples)

    # store name and chain size (proportional to evidence)
    samples.insert(len(samples.columns),'Source',source,True)
    samples.insert(len(samples.columns),'Chain Length',len(samples),True)
    samples_list.append(samples[['Source','Galactic Latitude','Galactic Longitude','Chain Length']])

# combine all source samples into one dataframe
all_sources = pd.concat(samples_list)

#%% 
# Produce healpix map of joint posterior
nside = 64
hpmap = lisacat.HPhist(all_sources,nside)
fig = plt.figure(figsize=(8, 6), dpi=100)

ax = plt.axes([0.05, 0.05, 0.9, 0.9],projection='geo degrees mollweide')
ax.grid()

# use logarithmic scaling for density
ax.imshow_hpx(np.log10(hpmap+1), cmap='plasma')



