"""
Parameter table
====================

Display `pandas` tables of catalog meta data, detections, point estimates for their parameters, and summaries of posterior samples.
This example also serves as a brief tutorial for using the `lisacattools.catalog` tools
"""

import pandas as pd
from lisacattools.catalog import GWCatalogs, GWCatalogType

#%%
# Start by loading the main catalog files processed from GBMCMC outputs
#

catType = GWCatalogType.UCB   # catalog type (UCB or MBH)
catPath = "../../tutorial/data/ucb" # path to catalog files
catName = "cat15728640_v2.h5" # name of specific catalog file
catPattern = "/cat**.h5"       # pattern of main catalog file(s) cat[T]_v[i].h5
rejPattern = "/*chains*"       # pattern of chain files cat[T]_v[i]_chains_[j]s.h5

# create catalogs object by searching for specifically-named files
catalogs = GWCatalogs.create(catType,
                             catPath,
                             accepted_pattern=catPattern,
                             rejected_pattern=rejPattern)

# or create catalogs object for specific file name
catalogs_specified = GWCatalogs.create(catType,catPath,catName)

#%%
# Get metadata of catalogs into `DataFrame`
metadata = catalogs.metadata
metadata.style

#%%
# Compare metadata to specified catalog
metadata = catalogs_specified.metadata
metadata.style

#%%
# Demonstrate some of the built in functions for the `GWCatalogs` object
#

# get list of catalogs' names
names = catalogs.get_catalogs_name()
print(names)

# select individual catelog by place in list (oldest)
cat_first = catalogs.get_first_catalog()

# select individual catelog by place in list (newest)
cat_last = catalogs.get_last_catalog()

# select individual catelog by name
cat_6mo = catalogs.get_catalog_by('aws_6mo_v2')

print(cat_first, cat_6mo, cat_last,sep="\n")

#%%
# Demonstrate some of the built in functions for the `GWCatalog` object
#

catalog = catalogs.get_catalog_by('aws_6mo_v2')

# get list of attributes for each detection in catalog object
list_of_attributes = catalog.get_attr_detections()
print("list of attributes:")
print(*list_of_attributes,sep="\n")

#get list of detections in catalog
detections_list = catalog.get_detections()
print("\nlist of 1st 10 detections:")
print(*detections_list[:10],sep="\n")

#get DataFrame of all detectiona
detections_df = catalog.get_dataset("detections")
detections_df.sort_values(by='SNR',ascending=False)


#%%
# Here are a few ways to select individual sources based on their
# observed properties
#

# catalog.get_median_source() returns pandas DataFrame of detection metadata
median_snr_source = catalog.get_median_source('SNR')
median_f0_source = catalog.get_median_source('Frequency')
median_A_source = catalog.get_median_source('Amplitude')

pd.concat([median_snr_source,median_A_source,median_f0_source]).style

#%%
# Now pick a single source and investigate it's parameters
#

# choose median SNR source for deeper analysis
sourceID = median_snr_source.index[0]

# get list of samples attributes
sample_attr = catalog.get_attr_source_sample(sourceID)
print("\nlist of posterior sample parameters:")
print(*sample_attr,sep="\n")

# get all posterior samples in a pandas DataFrame
samples = catalog.get_source_sample(sourceID)
samples.describe()

#%%
# It is easy to pick out a subset of parameters
# (i.e. marginalize over all others)
#

# get subset (i.e. marginalized) of samples
parameters = ['Frequency','Amplitude','Ecliptic Longitude','Ecliptic Latitude']
marginalized_samples = catalog.get_source_sample(sourceID,parameters)
marginalized_samples.describe()
