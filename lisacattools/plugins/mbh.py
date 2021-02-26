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
"""Module implemented the MBH catalog."""
import glob
import logging
import os
from typing import List, Union

import numpy as np
import pandas as pd

from ..catalog import GWCatalog, GWCatalogs, UtilsLogs, UtilsMonitoring

UtilsLogs.addLoggingLevel("TRACE", 15)


class LisaCatalogs(GWCatalogs):
    """Implementation of the LISA catalogs."""

    def __init__(self, path: str, pattern: str = "MBH_wk*C.h5"):
        """Init the LisaCatalogs by reading all catalogs with a specific
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
        self.__metadata = self.__metadata.sort_values(by="observation week")

    @UtilsMonitoring.io(level=logging.DEBUG)
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
        __doc__ = GWCatalogs.metadata.__doc__
        return self.__metadata

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def count(self) -> int:
        __doc__ = GWCatalogs.count.__doc__
        return len(self.metadata.index)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalogs_name(self) -> List[str]:
        __doc__ = GWCatalogs.get_catalogs_name.__doc__
        return list(self.metadata.index)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_first_catalog(self) -> GWCatalog:
        __doc__ = GWCatalogs.get_first_catalog.__doc__
        location = self.metadata.iloc[0]["location"]
        name = self.metadata.index[0]
        return LisaCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_last_catalog(self) -> GWCatalog:
        __doc__ = GWCatalogs.get_last_catalog.__doc__
        location = self.metadata.iloc[self.count - 1]["location"]
        name = self.metadata.index[self.count - 1]
        return LisaCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalog(self, idx: int) -> GWCatalog:
        __doc__ = GWCatalogs.get_catalog.__doc__
        location = self.metadata.iloc[idx]["location"]
        name = self.metadata.index[idx]
        return LisaCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalog_by(self, name: str) -> GWCatalog:
        __doc__ = GWCatalogs.get_catalog_by.__doc__
        cat_idx = self.metadata.index.get_loc(name)
        return self.get_catalog(cat_idx)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_lineage(self, cat_name: str, src_name: str) -> pd.DataFrame:
        __doc__ = GWCatalogs.get_lineage.__doc__

        dfs = list()
        while src_name != "" and cat_name not in [None, ""]:
            detections = self.get_catalog_by(cat_name).get_dataset(
                "detections"
            )
            src = detections.loc[[src_name]]
            try:
                wk = self.metadata.loc[cat_name]["observation week"]
            except:
                wk = self.metadata.loc[cat_name]["Observation Week"]

            src.insert(0, "Observation Week", wk, True)
            src.insert(1, "Catalog", cat_name, True)
            dfs.append(src)
            try:
                prnt = self.metadata.loc[cat_name]["parent"]
            except:
                prnt = self.metadata.loc[cat_name]["Parent"]

            cat_name = prnt
            src_name = src.iloc[0]["Parent"]

        histDF = pd.concat(dfs, axis=0)
        histDF.drop_duplicates(
            subset="Log Likelihood", keep="last", inplace=True
        )
        histDF.sort_values(by="Observation Week", ascending=True, inplace=True)
        return histDF

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_lineage_data(self, lineage: pd.DataFrame) -> pd.DataFrame:
        __doc__ = GWCatalogs.get_lineage_data.__doc__

        def _process_lineage(source_epoch, source_data, obs_week):
            source_data.insert(
                len(source_data.columns), "Source", source_epoch, True
            )
            source_data.insert(
                len(source_data.columns), "Observation Week", obs_week, True
            )
            return source_data

        source_epochs = list(lineage.index)

        merge_source_epochs = pd.concat(
            [
                _process_lineage(
                    source_epoch,
                    self.get_catalog_by(
                        lineage.loc[source_epoch]["Catalog"]
                    ).get_source_sample(source_epoch),
                    lineage.loc[source_epoch]["Observation Week"],
                )
                for source_epoch in source_epochs
            ]
        )
        merge_source_epochs = merge_source_epochs[
            [
                "Source",
                "Observation Week",
                "Mass 1",
                "Mass 2",
                "Spin 1",
                "Spin 2",
                "Ecliptic Latitude",
                "Ecliptic Longitude",
                "Luminosity Distance",
                "Barycenter Merge Time",
                "Merger Phase",
                "Polarization",
                "cos inclination",
            ]
        ].copy()
        return merge_source_epochs

    def __repr__(self):
        return f"LisaCatalogs({self.path!r}, {self.pattern!r})"

    def __str__(self):
        return f"LisaCatalogs: {self.path} {self.pattern}"


class LisaCatalog(GWCatalog):
    """Implementation of the LISA catalog."""

    def __init__(self, name: str, location: str):
        """Init the LISA catalog with a name and a location

        Args:
            name (str): name of the catalog
            location (str): location of the catalog
        """
        self.__name = name
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
    def get_detections(
        self, attr: List[str] = None
    ) -> Union[List[str], pd.DataFrame]:
        __doc__ = GWCatalog.get_detections.__doc__
        detections = self.get_dataset("detections")
        return (
            list(detections.index) if attr is None else detections[attr].copy()
        )

    @UtilsMonitoring.io(level=logging.DEBUG)
    def get_attr_detections(self) -> List[str]:
        __doc__ = GWCatalog.get_attr_detections.__doc__
        return list(self.get_dataset("detections").columns)

    @UtilsMonitoring.io(level=logging.DEBUG)
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
    def get_source_sample(
        self, source_name: str, attr: List[str] = None
    ) -> pd.DataFrame:
        __doc__ = GWCatalog.get_source_sample.__doc__
        samples = self.get_dataset(f"{source_name}_chain")
        return samples if attr is None else samples[attr].copy()

    @UtilsMonitoring.io(level=logging.DEBUG)
    def get_attr_source_sample(self, source_name: str) -> List[str]:
        __doc__ = GWCatalog.get_attr_source_sample.__doc__
        return list(self.get_dataset(f"{source_name}_chain").columns)

    @UtilsMonitoring.io(level=logging.TRACE)
    def describe_source_sample(self, source_name: str) -> pd.DataFrame:
        __doc__ = GWCatalog.describe_source_sample.__doc__
        return self.get_source_sample(source_name).describe()

    def __repr__(self):
        return f"LisaCatalog({self.__name!r}, {self.__location!r})"

    def __str__(self):
        return f"LisaCatalog: {self.__name} {self.__location}"
