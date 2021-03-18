"""
Connecting catalogs
===================

Locate a source in an updated catalog and compare parameters.
"""

#%%
# This example shows how to find a particular source after the catalog has been updated
# based on the `parent` meta data, and produces a corner plot showing how the parameter
# estimation evolves with time.

import pandas as pd
import numpy as np
from chainconsumer import ChainConsumer
from lisacattools.catalog import GWCatalog, GWCatalogs, GWCatalogType

#%%
# Start by loading the 03 month catalog and selecting a source to follow
catPath = "../../tutorial/data/ucb"
catName = "cat7864320_v3.h5"

meta_catalog = GWCatalogs.create(GWCatalogType.UCB, catPath, catName)
parent_catalog = meta_catalog.get_last_catalog()

detections_attr = parent_catalog.get_attr_detections()
parent_detections = parent_catalog.get_detections(detections_attr)

# pick a source, any source
parent_source = "LDC0027827268"

# use get_attr_source_sample() to return list
# of all parameters in samples dataframe
sample_attr = parent_catalog.get_attr_source_sample(parent_source)

#load full set of parameters
parent_samples = parent_catalog.get_source_sample(parent_source, sample_attr)

parent_detections.loc[[parent_source], ["SNR", "Frequency", "Amplitude"]]

#%%
# Load the 06 month catalog and find the current name for `parent_source`
catName = "cat15728640_v2.h5"

meta_catalog = GWCatalogs.create(GWCatalogType.UCB, catPath, catName)
child_catalog = meta_catalog.get_last_catalog()

child_detections = child_catalog.get_detections(detections_attr)

# select source that lists parent_source as parent
child_detections = child_detections[(child_detections["parent"] == parent_source)]
child_source = child_detections.index.values[0]

# load parameters of child source in new catalog
child_samples = child_catalog.get_source_sample(child_source, sample_attr)

child_detections.loc[[child_source], ["parent", "SNR", "Frequency", "Amplitude"]]

#%%
# Plot the posteriors for the 03 and 06 months inferences for the source

c = ChainConsumer()

# Select which parameters to plot & format the axes labels
parameters = [
    "Frequency",
    "Amplitude",
    "Ecliptic Longitude",
    "Ecliptic Latitude",
    "Inclination",
]
parameter_labels = [
    r"$f_0\ [{\rm Hz}]$",
    r"$\mathcal{A}$",
    r"$\phi\ [{\rm rad}]$",
    r"$\theta\ [{\rm rad}]$",
    r"$\iota\ [{\rm rad}]$",
]


# add chains
c.add_chain(
    parent_samples[parameters].values,
    parameters=parameter_labels,
    cloud=True,
    name=parent_source,
)
c.add_chain(
    child_samples[parameters].values,
    parameters=parameter_labels,
    cloud=True,
    name=child_source,
)

# plot!
c.configure(
    sigmas=[1, 2, 3],
    linestyles=["-", "--"],
    legend_color_text=False,
    legend_kwargs={"fontsize": 18},
)
fig = c.plotter.plot(figsize=1.5)
