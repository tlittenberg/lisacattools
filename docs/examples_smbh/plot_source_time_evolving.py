# -*- coding: utf-8 -*-
"""
Time-evolving parameter estimation
==================================

Corner plot of select parameters for a single source showing how
parameter estimation changes with observing time.
"""
import matplotlib.pyplot as plt
from chainconsumer import ChainConsumer, Chain, PlotConfig

from lisacattools.catalog import GWCatalogs
from lisacattools.catalog import GWCatalogType


# Find the list of catalogs
catPath = "../../tutorial/data/mbh"
catalogs = GWCatalogs.create(GWCatalogType.MBH, catPath, "*.h5")

last_cat = catalogs.get_last_catalog()
detections_attr = last_cat.get_attr_detections()
detections = last_cat.get_detections(detections_attr)

#%%
# Choose a source from the list of detections and get its history through the different catalogs
# Pick a source, any source
sourceIdx = "MBH005546845"

#%%
# Load chains for different observing epochs of selected source
# Get source history and display table with parameters and observing weeks containing source
srcHist = catalogs.get_lineage(last_cat.name, sourceIdx)
srcHist.drop_duplicates(subset="Log Likelihood", keep="last", inplace=True)
srcHist.sort_values(by="Observation Week", ascending=True, inplace=True)
srcHist[
    [
        "Observation Week",
        "Parent",
        "Log Likelihood",
        "Mass 1",
        "Mass 2",
        "Luminosity Distance",
    ]
]

# Load chains for different observing epochs of selected source
allEpochs = catalogs.get_lineage_data(srcHist)

#%%
# Create corner for multiple observing epochs

# Choose weeks for plot from source history table
wks = [4, 8, 10]

# select subset of parameters to plot
parameters = ["Mass 1", "Mass 2", "Luminosity Distance"]

labels = {
    parameters[0]: r"$m_1\ [{\rm M}_\odot]$",
    parameters[1]:r"$m_2\ [{\rm M}_\odot]$",
    parameters[2]:r"$D_L\ [{\rm Gpc}]$"
}

c = ChainConsumer()
for idx, wk in enumerate(wks):
    epoch = allEpochs[allEpochs["Observation Week"] == wk]
    samples = epoch[parameters]
    samples
    c.add_chain(Chain(samples=samples, name="Week " + str(wk), cmap="plasma"))

c.set_plot_config(
    PlotConfig(
        plot_hists=False,
        labels = labels,
        log_scales=[parameters[0], parameters[1]],
        extents={
            parameters[0]:(10000, 50000),
            parameters[1]:(1000, 5000),
            parameters[2]:(16, 40)
        }
    )
)
fig = c.plotter.plot(figsize=1.5)
plt.show()
