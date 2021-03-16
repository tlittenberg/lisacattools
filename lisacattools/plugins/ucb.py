# Copyright (C) 2021 - James I. Thorpe, Tyson B. Littenberg, Jean-Christophe
# Malapert
#
# This file is part of lisacattools.
#
# lisacattools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lisacattools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lisacattools.  If not, see <https://www.gnu.org/licenses/>.
"""Module implemented the UCB catalog."""

import glob
import os
from typing import List, Union

import logging
import numpy as np
import pandas as pd

from ..catalog import GWCatalog, GWCatalogs, UtilsMonitoring, UtilsLogs

UtilsLogs.addLoggingLevel("TRACE", 15)


class UcbCatalogs(GWCatalogs):
    """Implementation of the UCB catalogs."""

    def __init__(self, path: str, pattern: str = "*.h5"):
        """Init the UcbCatalogs by reading all catalogs with a specific
        pattern in a given directory.

        The list of catalogs is sorted by "observation week"

        Args:
            path (str): directory
            pattern (str, optional): pattern. Defaults to "MBH_wk*C.h5".
        """
        self.path = path
        self.pattern = pattern
        cat_files = glob.glob(path + os.path.sep + pattern)
        self.__metadata = pd.concat(
            [self._read_cats(cat_file) for cat_file in cat_files]
        )
        self.__metadata = self.__metadata.sort_values(by="Observation Time")

    def _read_cats(self, cat_file: str) -> pd.DataFrame:
        """Reads the metadata of a given catalog and the location of the file.

        Args:
            cat_file (str): catalog to load
            pattern (str) : pattern to be used when the catalog is a tar

        Returns:
            pd.DataFrame: pandas data frame
        """
        df = pd.read_hdf(cat_file, key="metadata")
        df["location"] = cat_file
        return df

    @property
    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def metadata(self) -> pd.DataFrame:
        __doc__ = GWCatalogs.metadata.__doc__
        return self.__metadata

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def count(self) -> int:
        __doc__ = GWCatalogs.count.__doc__
        return len(self.metadata.index)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_catalogs_name(self) -> List[str]:
        __doc__ = GWCatalogs.get_catalogs_name.__doc__
        return list(self.metadata.index)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_first_catalog(self) -> GWCatalog:
        __doc__ = GWCatalogs.get_first_catalog.__doc__
        location = self.metadata.iloc[0]["location"]
        name = self.metadata.index[0]
        return UcbCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_last_catalog(self) -> GWCatalog:
        __doc__ = GWCatalogs.get_last_catalog.__doc__
        location = self.metadata.iloc[self.count - 1]["location"]
        name = self.metadata.index[self.count - 1]
        return UcbCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_catalog(self, idx: int) -> GWCatalog:
        __doc__ = GWCatalogs.get_catalog.__doc__
        location = self.metadata.iloc[idx]["location"]
        name = self.metadata.index[idx]
        return UcbCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_catalog_by(self, name: str) -> GWCatalog:
        __doc__ = GWCatalogs.get_catalog_by.__doc__
        cat_idx = self.metadata.index.get_loc(name)
        return self.get_catalog(cat_idx)

    def get_lineage(self, cat_name: str, src_name: str) -> pd.DataFrame:
        raise NotImplementedError(
            "Get_lineage is not implemented for this catalog !"
        )

    def get_lineage_data(self, lineage: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError(
            "Get_lineage_data is not implemented for this catalog !"
        )

    def __repr__(self):
        return f"UcbCatalogs({self.path!r}, {self.pattern!r})"

    def __str__(self):
        return f"UcbCatalogs: {self.path} {self.pattern}"


class UcbCatalog(GWCatalog):
    """Implementation of the Ucb catalog."""

    def __init__(self, catalog_name: str, location: str):
        """Init the LISA catalog with a name and a location

        Args:
            name (str): name of the catalog
            location (str): location of the catalog
        """
        self.__name = catalog_name
        self.__location = location
        store = pd.HDFStore(location)
        self.__datasets = store.keys()
        store.close()

    @property
    @UtilsMonitoring.io(level=logging.DEBUG)
    def datasets(self):
        """dataset.

        :getter: Returns the list of datasets
        :type: List
        """
        return self.__datasets

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_dataset(self, name: str) -> pd.DataFrame:
        """Returns a dataset based on its name.

        Args:
            name (str): name of the dataset

        Returns:
            pd.DataFrame: the dataset
        """
        return pd.read_hdf(self.location, key=name)

    @property
    @UtilsMonitoring.io(level=logging.DEBUG)
    def name(self) -> str:
        __doc__ = GWCatalog.name.__doc__
        return self.__name

    @property
    @UtilsMonitoring.io(level=logging.DEBUG)
    def location(self) -> str:
        __doc__ = GWCatalog.location.__doc__
        return self.__location

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_detections(
        self, attr: List[str] = None
    ) -> Union[List[str], pd.DataFrame]:
        __doc__ = GWCatalog.get_detections.__doc__
        detections = self.get_dataset("detections")
        return (
            list(detections.index) if attr is None else detections[attr].copy()
        )

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_attr_detections(self) -> List[str]:
        __doc__ = GWCatalog.get_attr_detections.__doc__
        return list(self.get_dataset("detections").columns)

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_median_source(self, attr: str) -> pd.DataFrame:
        __doc__ = GWCatalog.get_median_source.__doc__
        val = self.get_detections(attr)
        source_idx = self.get_detections()[
            np.argmin(np.abs(np.array(val) - val.median()))
        ]
        return self.get_detections(self.get_attr_detections()).loc[
            [source_idx]
        ]

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_source_sample(
        self, source_name: str, attr: List[str] = None
    ) -> pd.DataFrame:
        __doc__ = GWCatalog.get_source_sample.__doc__
        samples = self.get_detections(["chain file"])
        chain_file = samples.loc[source_name]["chain file"]
        dirname = os.path.dirname(self.location)
        source_sample_file = os.path.join(dirname, chain_file)
        source_sample = pd.read_hdf(
            source_sample_file, key=f"{source_name}_chain"
        )
        return source_sample if attr is None else source_sample[attr].copy()

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG)
    def get_attr_source_sample(self, source_name: str) -> List[str]:
        __doc__ = GWCatalog.get_attr_source_sample.__doc__
        return list(self.get_source_sample(source_name).columns)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG)
    def describe_source_sample(self, source_name: str) -> pd.DataFrame:
        __doc__ = GWCatalog.describe_source_sample.__doc__
        return self.get_source_sample(source_name).describe()

    def __repr__(self):
        return f"UcbCatalog({self.__name!r}, {self.__location!r})"

    def __str__(self):
        return f"UcbCatalog: {self.__name} {self.__location}"