"""
3D map of the galaxy
=====================

Create inferred map of the galaxy from chirping binaries
"""

#%%
# This example demonstrates using chirping binaries to map the galaxy. 
# Samples from the high SNR chirping binaries are reparameterized into galactic cartesian coordinates and plotted.

# Import modules
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.colors as colors
import matplotlib.cm as cm
import lisacattools.lisacattools as lisacat

# Start by loading the main catalog file processed from GBMCMC outputs
catFile = 'cat15728640_v2/cat15728640_v2.h5'
catPath = os.path.split(catFile)[0]
cat = pd.read_hdf(catFile, key='detections')

# Get dataframe of only high SNR chirping events
cat_chirping = cat[(cat['Frequency Derivative']>0) & (cat['SNR']>100)]

# set up the figure
fig,axs = plt.subplots(1,2,figsize=(12, 6), dpi = 100)

axs[0].grid()
axs[1].grid()

axs[0].set(xlim=(-10,10), ylim=(-10,10), xlabel=r'$x_{\rm GC}\ [{\rm kpc}]$', ylabel=r'$y_{\rm GC}\ [{\rm kpc}]$')
axs[1].set(xlim=(-10,10), ylim=(-10,10), xlabel=r'$x_{\rm GC}\ [{\rm kpc}]$', ylabel=r'$z_{\rm GC}\ [{\rm kpc}]$')


# color ellipses by log SNR
cNorm = colors.LogNorm(vmin=cat_chirping['SNR'].min(), vmax=cat_chirping['SNR'].max())
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=plt.cm.get_cmap('plasma_r'))
cbar = fig.colorbar(scalarMap)
cbar.set_label('SNR')

# plot 1-sigma ellipses of 3D localization for each source
sources = list(cat_chirping.index)
for source in sources:
    
    # get chain samples
    samples = lisacat.getChain(cat_chirping,source,catPath)
    
    # convert from ecliptic to galactic coordinates
    lisacat.getGalcoord(samples)

    # enforce GR prior
    samples = samples[(samples['Frequency Derivative']>0)]
    
    # add distance parameter
    lisacat.get_DL(samples)
    
    # add galactic cartesian coordinates
    samples['X'] = samples['Luminosity Distance']*np.cos(samples['Galactic Latitude']*np.pi/180.)*np.cos(samples['Galactic Longitude']*np.pi/180.)
    samples['Y'] = samples['Luminosity Distance']*np.cos(samples['Galactic Latitude']*np.pi/180.)*np.sin(samples['Galactic Longitude']*np.pi/180.)
    samples['Z'] = samples['Luminosity Distance']*np.sin(samples['Galactic Latitude']*np.pi/180.)

    # plot galactic X-Y plane
    lisacat.confidence_ellipse(samples[['X','Y']],
                       axs[0],
                       n_std = 1.0,
                       edgecolor=scalarMap.to_rgba(np.array(cat_chirping.loc[source].SNR)),
                       linewidth = 1.0)

    # plot galactic X-Z plane
    lisacat.confidence_ellipse(samples[['X','Z']],
                       axs[1],
                       n_std = 1.0,
                       edgecolor=scalarMap.to_rgba(np.array(cat_chirping.loc[source].SNR)),
                       linewidth = 1.0)



plt.show()
