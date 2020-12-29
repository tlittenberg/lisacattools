"""
Scatter plots
========================

Display a scatter plot of detections' point estimates.
"""

import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import lisacattools.lisacattools as lisacat

#load catalog
catFile = 'cat15728640_v2/cat15728640_v2.h5'
cat = pd.read_hdf(catFile, key='detections')
meta = pd.read_hdf(catFile, key='metadata')

#set up matplotlib figure
fig = plt.figure(figsize=(12, 6), dpi = 100)
ax = plt.axes()

plt.yscale('log')
plt.xscale('log')
plt.xlabel('Frequency [Hz]',fontsize=14)
plt.ylabel('Strain Amplitude',fontsize=14)
plt.title('Point estimates for %i sources found in catalog %s' % (len(cat), meta.index[0]),fontsize=18)

#color points in scatter plot by SNR
cNorm = colors.LogNorm(vmin=cat['SNR'].min(), vmax=cat['SNR'].max()) #re-wrapping normalization
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=plt.cm.get_cmap('cool'))
cbar = fig.colorbar(scalarMap)
cbar.set_label('SNR',fontsize=14)


#the scatter plot
cat.plot(
    kind='scatter', 
    x='Frequency', 
    y='Amplitude',  
    marker = '.',
    c = scalarMap.to_rgba(np.array(cat['SNR'])),
    ax = ax);

#add sensitivity curve
f = np.logspace(-4,0,512)
ax.plot(f,lisacat.getSciRD(f,np.float(meta.iloc[0]['Observation Time'])), color='k')
ax.legend(['Instrument Sensitivity','resolved GBs'],fontsize=14)
ax.grid()

plt.show()



