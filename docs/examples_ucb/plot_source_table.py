"""
Parameter table
====================

Display a table of detections and point estimates for their parameters.
"""

import pandas as pd
import dataframe_image as dfi

#load parameter table and display top of data frame
df = pd.read_hdf('cat15728640_v2/cat15728640_v2.h5', key = 'detections')
df[['SNR','Frequency','Amplitude','Ecliptic Longitude','Ecliptic Latitude','Inclination']].head()
