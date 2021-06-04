"""
Select EM Candidates
=========================

Select candidates for EM follow-up based on localization, galactic latitude, and inclination.
"""

#%%
# Load catalog and compute sky areas
import numpy as np
import matplotlib.pyplot as plt
from lisacattools.catalog import GWCatalogs, GWCatalogType
from lisacattools import convert_ecliptic_to_galactic, ellipse_area, confidence_ellipse

# Start by loading the main catalog file processed from GBMCMC outputs
catPath = "../../tutorial/data/ucb"
catalogs = GWCatalogs.create(GWCatalogType.UCB, catPath, "cat15728640_v2.h5")
catalog = catalogs.get_last_catalog()

# Get full dataframe of detections metadata
detections_attr = catalog.get_attr_detections()
detections = catalog.get_detections(detections_attr)

# loop through all of the sources, compute sky area and median
# galactic lat. and lon., and add as a columns to the catalog metadata
area = np.empty(len(detections.index))
lat = np.empty(len(detections.index))
lon = np.empty(len(detections.index))

sources = list(detections.index)
for idx, source in enumerate(sources):
    
    # load source chain
    samples = catalog.get_source_samples(source)

    # correct sign error in catalog production
    samples['Ecliptic Latitude'] = np.pi/2 - np.arccos(samples['coslat'])

    # convert from ecliptic to galactic coordinates
    convert_ecliptic_to_galactic(samples)

    # create numpy arrays of the derived parameters
    area[idx] = ellipse_area(samples[["Galactic Longitude", "Galactic Latitude"]])

    # create numpy array of median galactic latitude
    lat[idx] = samples['Galactic Latitude'].median()
    
    # create numpy array of median galactic longitude
    lon[idx] = samples['Galactic Longitude'].median()

# insert new numpy arrays into main catalog dataframe
detections.insert(len(detections.columns), "Sky Area", area, True)
detections.insert(len(detections.columns), "Galactic Latitude", lat, True)
detections.insert(len(detections.columns), "Galactic Longitude", lon, True)

# create new columns with Inclination in degrees and orbital period
detections['Inclination'] = np.arccos(np.absolute(detections['cosinc']))*180/np.pi
detections['Period'] = 0.5/detections['Frequency']/60.


#%%
# Make new source catalog of EM follow-up candidates.
# Cut source catalog on:
#   * Localization (<100 sq deg)
#   * Galactic latitude (above or below 20 deg)
#   * Inclination (> 20 deg)

# Define thresholds for follow-up candidates
max_sky_area = 100  # localization threshold (square degrees)
min_lat = 30 # galactic latitude cut (+/-degrees)
min_inc = 20 # inclination threshold (degrees)

# Make new dataframe containing only "well-localized" events
candidates = detections[
    (detections["Sky Area"] < max_sky_area) & # Must be well localized...
    (np.absolute(detections["Galactic Latitude"]) > min_lat) & # ...above/below the galactic plane...
    (detections["Inclination"] > min_inc ) # ...and sufficiently to show some light curve variability
]

# Display table of follow-up candidates
candidates[['Period','Sky Area','Galactic Latitude','Galactic Longitude','Inclination']]

#%%
# Plot sky localization posteriors for each follow-up candidate.
# Figure is dynamically set up based on the number of sources.

# how many sources?
N = len(candidates.index)

# plot will be nxn large, must be at least 2x2 for subplot
n = max(2,int(np.ceil(np.sqrt(N))))

# set up figure
fig,axs = plt.subplots(n,n,figsize=(n*3, n*3))
cmap = plt.get_cmap("Set2")
rgb_cm = cmap.colors  # returns array-like color

# loop over all sources adding panel for each sources
sources = list(candidates.index)
for idx,source in enumerate(sources):
    
    # subplot coordinates
    i = int(idx/n)
    j = int(idx-i*n)
    ax = axs[i,j]
    
    # color index
    c = idx%len(rgb_cm)
    color = rgb_cm[c]
    
    # get chain samples
    samples = catalog.get_source_samples(source)

    # correct sign error in catalog production
    samples['Ecliptic Latitude'] = np.pi/2 - np.arccos(samples['coslat'])

    # convert from ecliptic to galactic coordinates
    convert_ecliptic_to_galactic(samples)

    # get centroid and 1-sigma contours in galactic coordinates, add to plot
    galactic_coordinates = samples[['Galactic Longitude','Galactic Latitude']]

    axs[i,j].autoscale()
    axs[i,j].grid()
    axs[i,j].set(
        title = source,
        xlabel="Galactic Longitude [deg]",
        ylabel="Galactic Latitude [deg]",
    )

    confidence_ellipse( galactic_coordinates, ax, edgecolor=color, n_std=1)
    confidence_ellipse( galactic_coordinates, ax, edgecolor=color, n_std=2)
    confidence_ellipse( galactic_coordinates, ax, edgecolor=color, n_std=3)

# turn off unused panels
for idx in range(N, n*n):
    
    i = int(idx/n)
    j = int(idx-i*n)
    axs[i,j].axis('off')
    
# keep the axes labels from being too crowded
plt.subplots_adjust(wspace=0.5, hspace=0.5)

plt.show()
