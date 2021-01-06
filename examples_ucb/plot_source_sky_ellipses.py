"""
Sky Localization Ellipses
=========================

Plot 1-sigma contours of well-localized sources' sky location in galactic coordinates.
"""

#%% 
# Load catalog and compute sky areas
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

# loop through all of the sources, compute sky area, and add as a column to the catalog 
area = np.empty(len(cat))

sources = list(cat.index)
for idx,source in enumerate(sources):
    
    # load source chain
    df = lisacat.getChain(cat,source,catPath) 
    
    # convert from ecliptic to galactic coordinates
    lisacat.getGalcoord(df) 
    
    # create numpy arrays of the derived parameters
    area[idx] = lisacat.ellipse_area(df[['Galactic Longitude','Galactic Latitude']])

# insert new numpy arrays into main catalog dataframe
cat.insert(len(cat.columns),'Sky Area',area,True)

# show that, indeed, Sky Area is now a column in the dataframe
cat[['SNR','Frequency','Sky Area']].head()

#%% 
# Cut source catalog on localization, and plot skymap of selected sources
# In this example we use 100 sq deg as the localization threshold
# 10 sq deg is more appropriate for EM follow-up, but makes for a 
# less interesting figure

# Make new dataframe containing only "well-localized" events
max_sky_area = 100 #localization threshold (square degrees)
cat_loc = cat[(cat['Sky Area']<max_sky_area)] #cut sources based on max_sky_area

# set up the figure
fig = plt.figure(figsize=(12, 6), dpi = 100)
ax = plt.axes()

ax.grid()
ax.set(xlim=(-180,180), ylim=(-90,90), xlabel='Galactic Longitude', ylabel='Galactic Latitude')

# color ellipses by log frequency
cNorm = colors.LogNorm(vmin=cat_loc['Frequency'].min(), vmax=cat_loc['Frequency'].max()) 
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=plt.cm.get_cmap('viridis_r'))
cbar = fig.colorbar(scalarMap)
cbar.set_label('Frequency [Hz]')

# loop over all sources adding ellipse to plot
sources = list(cat_loc.index)
for source in sources:
    
    #get chain samples
    samples = lisacat.getChain(cat_loc,source,catPath)
    
    #convert from ecliptic to galactic coordinates
    lisacat.getGalcoord(samples)
    
    #get centroid and 1-sigma contours in galactic coordinates, add to plot
    m = np.array(samples[['Galactic Longitude','Galactic Latitude']].mean())
    lisacat.confidence_ellipse(samples[['Galactic Longitude','Galactic Latitude']], 
                       ax, 
                       n_std = 1.0, 
                       edgecolor=scalarMap.to_rgba(np.array(cat_loc.loc[source].Frequency)),
                       linewidth = 1.0)
                       
plt.show()
