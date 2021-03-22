#!/usr/bin/env python3
from lisacattools import GWCatalogs, GWCatalogType


class TestPluginUcb:
    def __init__(self):
        self.plugin = GWCatalogs.create(GWCatalogType.UCB, "tutorial/data/ucb")

    def get_number(self):
        return len(self.plugin.files)
