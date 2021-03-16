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
import ligo.skymap.plot
import matplotlib.pyplot as plt
from lisacattools.catalog import GWCatalogs, GWCatalogType
from lisacattools import convert_ecliptic_to_galactic, HPhist

# Start by loading the main catalog file processed from GBMCMC outputs
catPath = "../../tutorial/data/ucb"
catalogs = GWCatalogs.create(GWCatalogType.UCB, catPath, "cat15728640_v2.h5")
final_catalog = catalogs.get_last_catalog()
detections_attr = final_catalog.get_attr_detections()
detections = final_catalog.get_detections(detections_attr)


# loop over all sources in catalog and append chain samples to new dataframe
sources = list(detections.index)
samples_list = list()
for source in sources:

    # get chain samples
    samples = final_catalog.get_source_sample(source)

    # store name and chain size (proportional to evidence)
    samples.insert(len(samples.columns), "Source", source, True)
    samples.insert(len(samples.columns), "Chain Length", len(samples), True)
    samples_list.append(
        samples[["Source", "Ecliptic Latitude", "Ecliptic Longitude", "Chain Length"]]
    )

# combine all source samples into one dataframe
all_sources = pd.concat(samples_list)

#%%
# Produce healpix map of joint posterior
nside = 64
hpmap = HPhist(all_sources, nside)
fig = plt.figure(figsize=(8, 6), dpi=100)

ax = plt.axes([0.05, 0.05, 0.9, 0.9], projection="geo degrees mollweide")
ax.grid()

# use logarithmic scaling for density
ax.imshow_hpx(np.log10(hpmap + 1), cmap="plasma")
plt.show()
