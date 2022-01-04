#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lisacattools import GWCatalogs
from lisacattools import GWCatalogType


class TestCacheDoesNotCacheWrongElt:
    def __init__(self):
        catalogs = GWCatalogs.create(
            GWCatalogType.UCB, "tutorial/data/ucb", "cat15728640_v2.h5"
        )
        catalog = catalogs.get_last_catalog()
        c1 = catalog.get_source_samples("LDC0081497609")[
            ["Ecliptic Latitude", "Ecliptic Longitude"]
        ]
        c2 = catalog.get_source_samples("LDC0081535331")[
            ["Ecliptic Latitude", "Ecliptic Longitude"]
        ]
        min_c1_lat = c1.describe().min()[0]
        min_c1_long = c1.describe().min()[1]
        min_c2_lat = c2.describe().min()[0]
        min_c2_long = c2.describe().min()[1]
        self.compare = min_c1_lat == min_c2_lat and min_c1_long == min_c2_long

    def get_equal(self):
        return self.compare
