# -*- coding: utf-8 -*-
"""
Parameter tables
====================

Display `pandas` tables of catalog meta data, detections, point estimates for their parameters, and summaries of posterior samples.
This example also serves as a brief tutorial for using the `lisacattools.catalog` tools
"""
import pandas as pd

from lisacattools.catalog import GWCatalogs
from lisacattools.catalog import GWCatalogType

#%%
# Start by loading the main catalog files processed from GBMCMC outputs
#

catType = GWCatalogType.UCB  # catalog type (UCB or MBH)
catPath = "../../tutorial/data/ucb"  # path to catalog files
catName = "cat15728640_v2.h5"  # name of specific catalog file
catPattern = "/cat**.h5"  # pattern of main catalog file(s) cat[T]_v[i].h5
rejPattern = "/*chains*"  # pattern of chain files cat[T]_v[i]_chains_[j]s.h5

# create catalogs object by searching for specifically-named files
catalogs = GWCatalogs.create(
    catType, catPath, accepted_pattern=catPattern, rejected_pattern=rejPattern
)

# or create catalogs object for specific file name
catalogs_specified = GWCatalogs.create(catType, catPath, catName)

#%%
# Get metadata of catalogs into `DataFrame`
catalogs.metadata

#%%
# Compare metadata to specified catalog
catalogs_specified.metadata

#%%
# `GWCatalogs` object
# -------------------
#
# The `GWCatalogs` object can contain multiple catalogs
# (e.g. updated releases after more data are analyzed)

# Get list of catalogs' names
names = catalogs.get_catalogs_name()
print(names)

#%%
# Select individual catelogs...

# ...by place in list (oldest)
cat_first = catalogs.get_first_catalog()

# ...by place in list (newest)
cat_last = catalogs.get_last_catalog()

# ...by name
cat_6mo = catalogs.get_catalog_by("aws_6mo_v2")

print(cat_first, cat_6mo, cat_last, sep="\n")

#%%
# `GWCatalog` object
# ------------------
#
# Once an individual catalog is selected, explore some of the
# metadata it contains

# Select the 6-months release
catalog = catalogs.get_catalog_by("aws_6mo_v2")

#%%
# Get list of detections in catalog
detections_list = catalog.get_detections()
N_detections = len(detections_list)
print("\nlist of 1st 10 detections ({} total):\n".format(N_detections))
print(*detections_list[:10], sep="\n")

#%%
# Get list of attributes for each detection in catalog object
list_of_attributes = catalog.get_attr_detections()
print("list of attributes:\n")
print(*list_of_attributes, sep="\n")

#%%
# Get DataFrame of all detections, sorted by SNR
detections_df = catalog.get_dataset("detections")
detections_df.sort_values(by="SNR", ascending=False)


#%%
# Individual sources
# ------------------
#
# Select sources based on their observed properties

# catalog.get_median_source() returns pandas DataFrame of detection metadata
median_snr_source = catalog.get_median_source("SNR")
median_f0_source = catalog.get_median_source("Frequency")
median_A_source = catalog.get_median_source("Amplitude")

pd.concat([median_snr_source, median_A_source, median_f0_source]).style

#%%
# Now pick a single source and investigate it's parameters
#

# Choose median SNR source for deeper analysis
sourceID = median_snr_source.index[0]

# get list of samples attributes
sample_attr = catalog.get_attr_source_samples(sourceID)
print(
    "\nlist of posterior sample parameters for source {}:\n".format(sourceID)
)
print(*sample_attr, sep="\n")

#%%
# Get all posterior samples in a pandas DataFrame,
# dropping redundant columns
samples = catalog.get_source_samples(sourceID).drop(
    ["coslat", "cosinc"], axis=1
)
samples.describe().loc[["mean", "std", "25%", "50%", "75%"]]

#%%
# It is easy to pick out a subset of parameters
# (i.e. marginalize over all others)
#

# get subset (i.e. marginalized) of samples
parameters = [
    "Frequency",
    "Amplitude",
    "Ecliptic Longitude",
    "Ecliptic Latitude",
    "Inclination",
]
marginalized_samples = catalog.get_source_samples(sourceID, parameters)
marginalized_samples.describe().loc[["mean", "std", "25%", "50%", "75%"]]
