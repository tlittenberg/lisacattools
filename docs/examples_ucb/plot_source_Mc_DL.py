# -*- coding: utf-8 -*-
"""
Resampling posteriors
=====================

Convert sampling parameters to derived parameters
"""
#%%
# This example shows how to change parameterization of the posterior samples.
# The GBMCMC sampler uses frequency, frequency derivative, and GW amplitude in its waveform model.
# For systems whose dynamics are driven by GR, those parameters can be converted to chirp mass and luminosity distance.
# Here is a demonstration of how to do that by producing a chirpmass-distance corner plot.
# Import modules
import matplotlib.pyplot as plt
from chainconsumer import ChainConsumer

from lisacattools import get_DL
from lisacattools import get_Mchirp
from lisacattools.catalog import GWCatalog
from lisacattools.catalog import GWCatalogs
from lisacattools.catalog import GWCatalogType

# Start by loading the main catalog file processed from GBMCMC outputs
catPath = "../../tutorial/data/ucb"
catalogs = GWCatalogs.create(GWCatalogType.UCB, catPath, "cat15728640_v2.h5")
final_catalog = catalogs.get_last_catalog()
detections_attr = final_catalog.get_attr_detections()
detections = final_catalog.get_detections(detections_attr)

# Sort table by SNR and select highest SNR source
detections.sort_values(by="SNR", ascending=False, inplace=True)
sourceId = detections.index[0]
samples = final_catalog.get_source_samples(sourceId)

# Reject chain samples with negative fdot (enforce GR-driven prior)
samples_GR = samples[(samples["Frequency Derivative"] > 0)]

# Add distance and chirpmass to samples
get_DL(samples_GR)
get_Mchirp(samples_GR)

# Make corner plot
parameters = ["Chirp Mass", "Luminosity Distance"]
parameter_symbols = [r"$\mathcal{M}\ [{\rm M}_\odot]$", r"$D_L\ [{\rm kpc}]$"]

df = samples_GR[parameters].values

c = ChainConsumer().add_chain(df, parameters=parameter_symbols, cloud=True)
c.configure(flip=False)
fig = c.plotter.plot(figsize=1.5)
plt.show()
