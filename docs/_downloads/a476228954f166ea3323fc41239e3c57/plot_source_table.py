"""
Detections table
====================

This example will demonstrate how to display a list of detections.
"""

import pandas as pd
import dataframe_image as dfi

#some comment
df = pd.read_hdf('../../Research/GalacticBinaries/Radler/06mo/cat15728640_v2/cat15728640_v2.h5', key = 'detections')
df[['SNR','Frequency','Amplitude','Ecliptic Longitude','Ecliptic Latitude','Inclination']].head()
