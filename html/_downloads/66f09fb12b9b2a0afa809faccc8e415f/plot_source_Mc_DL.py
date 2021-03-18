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
from chainconsumer import ChainConsumer
from lisacattools.catalog import GWCatalog, GWCatalogs, GWCatalogType
from lisacattools import get_DL, get_Mchirp

# Start by loading the main catalog file processed from GBMCMC outputs
catPath = "../../tutorial/data/ucb"
catFile = "cat15728640_v2.h5"
catalogs = GWCatalogs.create(GWCatalogType.UCB,catPath,catFile)
catalog = catalogs.get_last_catalog()

# Get SNR attribute for all detections
# Full list of attributes returned by catalog.get_attr_detections()
detections = catalog.get_detections(['SNR'])

# Sort list of detections by SNR and select loudest source
detections.sort_values(by="SNR",ascending=False, inplace=True)
sourceID = detections.index[0]
samples = catalog.get_source_sample(sourceID,['Frequency','Frequency Derivative','Amplitude'])

# Filter chain samples to reject negative fdot (enforce GR-only prior)
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

