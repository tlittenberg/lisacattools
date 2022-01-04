#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lisacattools import GWCatalogs
from lisacattools import GWCatalogType


class TestPluginMbh:
    def __init__(self):
        self.plugin = GWCatalogs.create(GWCatalogType.MBH, "tutorial/data/mbh")

    def get_number(self):
        return len(self.plugin.files)
