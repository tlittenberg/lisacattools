# -*- coding: utf-8 -*-
"""
Joint PDF of sky location
=========================

Plot joint posterior of all catalog sources in galactic coordinates.
"""
#%%
# Load catalogs and combine chain samples
import logging

import ligo.skymap.plot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from lisacattools import convert_ecliptic_to_galactic
from lisacattools import HPhist
from lisacattools import OFF
from lisacattools.catalog import GWCatalogs
from lisacattools.catalog import GWCatalogType

logger = logging.getLogger("lisacattools")
logger.setLevel(
    OFF
)  # Set the logger to OFF. By default, the logger is set to INFO

# Start by loading the main catalog file processed from GBMCMC outputs
catPath = "../../tutorial/data/ucb"
catalogs = GWCatalogs.create(GWCatalogType.UCB, catPath, "cat15728640_v2.h5")
catalog = catalogs.get_last_catalog()

# loop over all sources in catalog and append chain samples to new dataframe
sources = list(catalog.get_detections())

samples_list = list()
for source in sources:

    # get chain samples
    samples = catalog.get_source_samples(
        source, ["coslat", "Ecliptic Longitude"]
    )

    # recompute ecliptic latitude to correct error in HDF5 files
    samples["Ecliptic Latitude"] = np.pi / 2 - np.arccos(samples["coslat"])

    # append sky location parameters to joint posterior list
    samples_list.append(samples[["Ecliptic Latitude", "Ecliptic Longitude"]])

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
