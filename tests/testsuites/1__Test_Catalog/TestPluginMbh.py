#!/usr/bin/env python3
from lisacattools import GWCatalogs, GWCatalogType


class TestPluginMbh:
    def __init__(self):
        self.plugin = GWCatalogs.create(GWCatalogType.MBH, "tutorial/data/mbh")

    def get_number(self):
        return len(self.plugin.files)
