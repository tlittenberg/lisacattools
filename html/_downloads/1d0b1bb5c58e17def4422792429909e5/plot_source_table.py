"""
Parameter table
====================

Display a table of detections and point estimates for their parameters.
"""

import pandas as pd

# load parameter table and display top of data frame
df = pd.read_hdf("../../tutorial/data/ucb/cat15728640_v2.h5", key="detections")
df[
    [
        "SNR",
        "Frequency",
        "Amplitude",
        "Ecliptic Longitude",
        "Ecliptic Latitude",
        "Inclination",
    ]
].head()
