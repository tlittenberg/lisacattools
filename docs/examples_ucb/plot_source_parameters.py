# -*- coding: utf-8 -*-
"""
Corner plots
============

Produce corner plots for a single sources' parameters.
"""
#%%
# Load catalog and select individual source
import numpy as np

from lisacattools.catalog import GWCatalog
from lisacattools.catalog import GWCatalogs
from lisacattools.catalog import GWCatalogType

# load catalog
catPath = "../../tutorial/data/ucb"
catalogs = GWCatalogs.create(GWCatalogType.UCB, catPath, "cat15728640_v2.h5")
final_catalog = catalogs.get_last_catalog()
detections_attr = final_catalog.get_attr_detections()
detections = final_catalog.get_detections(detections_attr)

# get index of source with maximum SNR
sourceId = detections.index.values[
    np.argmin(np.abs(np.array(detections["SNR"]) - detections["SNR"].max()))
]
detections.loc[[sourceId], ["SNR", "Frequency"]]

#%%
# Corner plot of select source parameters using `corner` module

import corner
import matplotlib.pyplot as plt

# read in the chain samples for this source
samples = final_catalog.get_source_samples(sourceId)

# list of subset of paramters that are particularly interesting
parameters = ["Frequency", "Frequency Derivative", "Amplitude", "Inclination"]

# corner plot of source.
fig = corner.corner(samples[parameters])

#%%
# Can also be done with ChainConsumer for prettier plots
from chainconsumer import ChainConsumer, Chain, PlotConfig

# get dataframe into numpy array (this shouldn't be necessary)
df = samples[parameters]

# rescale columns
df[parameters[0]] *= 1000 # f in mHz
df[parameters[1]] /= 1e-15 # df/dt
df[parameters[2]] /= 1e-22 # A
df[parameters[3]] = df[parameters[3]] * 180.0 / np.pi # inc in deg

parameter_symbols = [
    r"$f\ {\rm [mHz]}$",
    r"$\dot{f}\ [s^{-2}]\times 10^{-16}$",
    r"$\mathcal{A} \times 10^{-23}$",
    r"$\iota\ {\rm [deg]}$",
]

labels =  {
    parameters[0]: parameter_symbols[0],
    parameters[1]: parameter_symbols[1],
    parameters[2]: parameter_symbols[2],
    parameters[3]: parameter_symbols[3]
}
# add source chain to ChainConsumer object
c = ChainConsumer()
c.add_chain(Chain(samples=df, name="Corner plots for a single sources' parameters", plot_cloud=True))


# plot!
c.set_plot_config(
    PlotConfig(
        labels = labels,
    )
)
fig = c.plotter.plot(figsize=1.5)
plt.show()
