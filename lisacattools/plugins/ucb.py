# -*- coding: utf-8 -*-
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
import logging
import os
from itertools import chain
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd

from ..catalog import GWCatalog
from ..catalog import GWCatalogs
from ..catalog import UtilsLogs
from ..catalog import UtilsMonitoring
from ..utils import CacheManager

UtilsLogs.addLoggingLevel("TRACE", 15)


class UcbCatalogs(GWCatalogs):
    """Implementation of the UCB catalogs."""

    EXTRA_DIR = "extra_directories"

    def __init__(
        self,
        path: str,
        accepted_pattern: Optional[str] = "*.h5",
        rejected_pattern: Optional[str] = "*chain*",
        *args,
        **kwargs,
    ):
        """Init the UcbCatalogs by reading all catalogs with a specific
        pattern in a given directory and rejecting files by another pattern.

        The list of catalogs is sorted by "observation week"

        Args:
            path (str): directory
            accepted_pattern (str, optional): pattern to accept files.
            Defaults to "*.h5".
            rejected_pattern (str, optional): pattern to reject files.
            Defaults to "*chain*".

        Raises:
            ValueError: no files found matching the accepted and rejected
            patterns.
        """
        self.path = path
        self.accepted_pattern = accepted_pattern
        self.rejected_pattern = rejected_pattern
        self.extra_directories = (
            kwargs[UcbCatalogs.EXTRA_DIR]
            if UcbCatalogs.EXTRA_DIR in kwargs
            else list()
        )
        directories = self._search_directories(
            self.path, self.extra_directories
        )
        self.cat_files = self._search_files(
            directories, accepted_pattern, rejected_pattern
        )
        if len(self.cat_files) == 0:
            raise ValueError(
                f"no files found matching the accepted \
                    ({self.accepted_pattern}) and rejected \
                    ({self.rejected_pattern}) patterns in {directories}"
            )
        self.__metadata = pd.concat(
            [self._read_cats(cat_file) for cat_file in self.cat_files]
        )
        self.__metadata = self.__metadata.sort_values(by="Observation Time")

    @UtilsMonitoring.io(level=logging.DEBUG)
    def _search_directories(
        self, path: str, extra_directories: List[str]
    ) -> List[str]:
        """Compute the list of directories on which the pattern will be applied.

        Args:
            path (str) : main path
            extra_directories (List[str]) : others directories

        Returns:
            List[str]: list of directories on which the pattern will be applied
        """
        directories: List[str] = extra_directories[:]
        directories.append(path)
        return directories

    @UtilsMonitoring.io(level=logging.DEBUG)
    def _search_files(
        self, directories: List[str], accepted_pattern, rejected_pattern
    ) -> List[str]:
        """Search files in directories according to a set of constraints :
        accepted and rejected patterns

        Args:
            directories (List[str]): List of directories to scan
            accepted_pattern ([type]): pattern to get files
            rejected_pattern ([type]): pattern to reject files

        Returns:
            List[str]: List of files
        """
        accepted_files = [
            glob.glob(path + os.path.sep + accepted_pattern)
            for path in directories
        ]
        accepted_files = list(chain(*accepted_files))
        if rejected_pattern is None:
            rejected_files = list()
        else:
            rejected_files = [
                list()
                if rejected_pattern is None
                else glob.glob(path + os.path.sep + rejected_pattern)
                for path in directories
            ]
        rejected_files = list(chain(*rejected_files))
        cat_files = list(set(accepted_files) - set(rejected_files))
        return cat_files

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
    def metadata(self) -> pd.DataFrame:
        __doc__ = GWCatalogs.metadata.__doc__  # noqa: F841
        return self.__metadata

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def count(self) -> int:
        __doc__ = GWCatalogs.count.__doc__  # noqa: F841
        return len(self.metadata.index)

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def files(self) -> List[str]:
        __doc__ = GWCatalogs.files.__doc__  # noqa: F841
        return self.cat_files

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalogs_name(self) -> List[str]:
        __doc__ = GWCatalogs.get_catalogs_name.__doc__  # noqa: F841
        return list(self.metadata.index)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_first_catalog(self) -> GWCatalog:
        __doc__ = GWCatalogs.get_first_catalog.__doc__  # noqa: F841
        location = self.metadata.iloc[0]["location"]
        name = self.metadata.index[0]
        return UcbCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_last_catalog(self) -> GWCatalog:
        __doc__ = GWCatalogs.get_last_catalog.__doc__  # noqa: F841
        location = self.metadata.iloc[self.count - 1]["location"]
        name = self.metadata.index[self.count - 1]
        return UcbCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_catalog(self, idx: int) -> GWCatalog:
        __doc__ = GWCatalogs.get_catalog.__doc__  # noqa: F841
        location = self.metadata.iloc[idx]["location"]
        name = self.metadata.index[idx]
        return UcbCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=10)
    def get_catalog_by(self, name: str) -> GWCatalog:
        __doc__ = GWCatalogs.get_catalog_by.__doc__  # noqa: F841
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
        return f"UcbCatalogs({self.path!r}, {self.accepted_pattern!r}, \
            {self.rejected_pattern!r}, {self.extra_directories!r})"

    def __str__(self):
        return f"UcbCatalogs: {self.path} {self.accepted_pattern!r} \
            {self.rejected_pattern!r} {self.extra_directories!r}"


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
        store = pd.HDFStore(location, "r")
        self.__datasets = store.keys()
        store.close()

    @CacheManager.get_cache_pandas(
        keycache_argument=[1, 2], level=logging.INFO
    )
    def _read_chain_file(
        self, source_name: str, chain_file: str
    ) -> pd.DataFrame:
        """Read a source in a chain_file

        Args:
            source_name (str): Name of the source to extract from the
            chain_file
            chain_file (str): file to load

        Returns:
            pd.DataFrame: [description]
        """
        dirname = os.path.dirname(self.location)
        source_samples_file = os.path.join(dirname, chain_file)
        source_samples = pd.read_hdf(
            source_samples_file, key=f"{source_name}_chain"
        )
        return source_samples

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
        __doc__ = GWCatalog.name.__doc__  # noqa: F841
        return self.__name

    @property
    @UtilsMonitoring.io(level=logging.DEBUG)
    def location(self) -> str:
        __doc__ = GWCatalog.location.__doc__  # noqa: F841
        return self.__location

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_detections(
        self, attr: Union[List[str], str] = None
    ) -> Union[List[str], pd.DataFrame, pd.Series]:
        __doc__ = GWCatalog.get_detections.__doc__  # noqa: F841
        detections = self.get_dataset("detections")
        return (
            list(detections.index) if attr is None else detections[attr].copy()
        )

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_attr_detections(self) -> List[str]:
        __doc__ = GWCatalog.get_attr_detections.__doc__  # noqa: F841
        return list(self.get_dataset("detections").columns)

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_median_source(self, attr: str) -> pd.DataFrame:
        __doc__ = GWCatalog.get_median_source.__doc__  # noqa: F841
        val = self.get_detections(attr)
        source_idx = self.get_detections()[
            np.argmin(np.abs(np.array(val) - val.median()))
        ]
        return self.get_detections(self.get_attr_detections()).loc[
            [source_idx]
        ]

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG, threshold_in_ms=100)
    def get_source_samples(
        self, source_name: str, attr: List[str] = None
    ) -> pd.DataFrame:
        __doc__ = GWCatalog.get_source_samples.__doc__  # noqa: F841
        samples: pd.DataFrame = self.get_detections(["chain file"])
        chain_file: str = samples.loc[source_name]["chain file"]
        source_samples = self._read_chain_file(source_name, chain_file)
        return source_samples if attr is None else source_samples[attr].copy()

    @UtilsMonitoring.io(level=logging.DEBUG)
    @UtilsMonitoring.time_spend(level=logging.DEBUG)
    def get_attr_source_samples(self, source_name: str) -> List[str]:
        __doc__ = GWCatalog.get_attr_source_samples.__doc__  # noqa: F841
        return list(self.get_source_samples(source_name).columns)

    @UtilsMonitoring.io(level=logging.TRACE)
    @UtilsMonitoring.time_spend(level=logging.DEBUG)
    def describe_source_samples(self, source_name: str) -> pd.DataFrame:
        __doc__ = GWCatalog.describe_source_samples.__doc__  # noqa: F841
        return self.get_source_samples(source_name).describe()

    def __repr__(self):
        return f"UcbCatalog({self.__name!r}, {self.__location!r})"

    def __str__(self):
        return f"UcbCatalog: {self.__name} {self.__location}"
