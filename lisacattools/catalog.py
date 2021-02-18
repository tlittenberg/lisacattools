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

"""This module is responsible for handling the loading of the LISA catalogs.
The LISA catalogs contains an evolution of catalogs over the time.
Each catalog contains several datasets :
- metadata
- detections
- sample for each detection
"""

import glob
import logging
import os
import pandas as pd
import numpy as np
from typing import List, Union
from .monitoring import UtilsMonitoring
from .custom_logging import UtilsLogs

UtilsLogs.addLoggingLevel("TRACE", 15)


class LisaCatalog:
    """Handling a Lisa catalog."""

    def __init__(self, catalog_name: str, location: str):
        """Init the loading of a Lisa catalog

        Args:
            catalog_name (str): name of the catalog
            location (str): location of the catalog
        """
        logging.getLogger().debug(
            """Init LisaCatalog with :
        - catalog_name: {catalog_name}
        - location: {location}
        """
        )
        self.__name = catalog_name
        self.__location = location
        store = pd.HDFStore(location)
        self.__datasets = store.keys()
        store.close()

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def name(self):
        """Catalog name.

        :getter: Returns the catalog name
        :type: str
        """
        return self.__name

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def location(self):
        """Location of the catalog.

        :getter: Returns the location of the catalog
        :type: str
        """
        return self.__location

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def datasets(self):
        """dataset.

        :getter: Returns the list of datasets
        :type: List
        """
        return self.__datasets

    @UtilsMonitoring.time_spend(level=logging.DEBUG)
    @UtilsMonitoring.io(level=logging.TRACE)
    def get_dataset(self, name: str) -> pd.DataFrame:
        """Returns a dataset based on its name.

        Args:
            name (str): name of the dataset

        Returns:
            pd.DataFrame: the dataset
        """
        return pd.read_hdf(self.location, key=name)

    @UtilsMonitoring.io(level=logging.TRACE)
    def describe_dataset(self, name: str) -> pd.DataFrame:
        """Describes a give dataset

        Args:
            name (str): dataset name to describe

        Returns:
            pd.DataFrame: statistics information on the dataset
        """
        return self.get_dataset(name).describe()

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_extracted_data_from(
        self, ds: str, keywords: Union[List, str]
    ) -> pd.DataFrame:
        """Returns the extracted keywords from the dataset.

        Args:
            ds (str): name of the dataset
            keywords (Union[List, str]): keyword(s) to extract

        Returns:
            pd.DataFrame: the dataset with the selected keyword(s)
        """
        return self.get_dataset(ds)[keywords].copy()

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_attributes_from(self, ds: str) -> List:
        """Returns the attributes of the dataset.

        Args:
            ds (str): dataset name

        Returns:
            List: the list of attributes
        """
        return list(self.get_dataset(ds).columns)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_median_source(self, ds: str, attribute: str) -> pd.DataFrame:
        """Returns the record for which we have computed the median of the attribute.

        Args:
            ds (str): dataset name
            attribute (Union[List, str]): [description]

        Returns:
            pd.DataFrame: the record
        """
        val = self.get_extracted_data_from(ds, attribute)
        sourceIdx = self.get_dataset(ds).index.values[
            np.argmin(np.abs(np.array(val) - val.median()))
        ]
        return self.get_dataset(ds).loc[[sourceIdx]]


class LisaCatalogs:
    """Handling the LISA catalogs over the time"""

    def __init__(self, path: str, pattern: str = "MBH_wk*C.h5"):
        """Init the loading of all the catalogs over the time according to the
        path of the data and the pattern to select the files to load.

        Args:
            path (str): location of the data
            pattern (str, optional): pattern to select the files to load. Defaults to 'MBH_wk*C.h5'.
        """
        logging.getLogger().debug(
            """Init LisaCatalogs with :
        - path: {path}
        - pattern: {pattern}
        """
        )
        cat_files = glob.glob(path + os.path.sep + pattern)
        logging.getLogger().debug(f"List of files to load {cat_files}")
        self.__metadata = pd.concat(
            [self._read_cats(cat_file) for cat_file in cat_files]
        )
        self.__metadata = self.__metadata.sort_values(by="observation week")
        logging.getLogger().info(
            f"LisaCatalogs has loaded {len(self.__metadata.index)} catalogs"
        )

    @UtilsMonitoring.time_spend(level=logging.DEBUG)
    @UtilsMonitoring.io(level=logging.TRACE)
    def _read_cats(self, cat_file: str) -> pd.DataFrame:
        """Reads the metadata of a given catalog and the location of the file.

        Args:
            cat_file (str): catalog to load

        Returns:
            pd.DataFrame: pandas data frame
        """
        df = pd.read_hdf(cat_file, key="metadata")
        df["location"] = cat_file
        return df

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def metadata(self):
        """metadata of the catalogs.

        :getter: Returns the metadata of the LISA catalogs
        :type: pd.DataFrame
        """
        return self.__metadata

    @property
    @UtilsMonitoring.io(level=logging.TRACE)
    def count(self):
        """Count the number of catalogs.

        :getter: Returns the number of loaded LISA catalogs
        :type: int
        """
        return len(self.metadata)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalogs_name(self) -> List:
        """Returns the name of each catalog in the LISA catalogs as a list

        Returns:
            List: name of each catalog
        """
        return list(self.metadata.index)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_first_catalog(self) -> LisaCatalog:
        """Returns the first catalog.

        Returns:
            LisaCatalog: the old one catalog
        """
        location = self.metadata.iloc[0]["location"]
        name = self.metadata.index[0]
        return LisaCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_last_catalog(self) -> LisaCatalog:
        """Returns the last catalog.

        Returns:
            LisaCatalog: the recent one catalog
        """
        location = self.metadata.iloc[self.count - 1]["location"]
        name = self.metadata.index[self.count - 1]
        return LisaCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalog(self, idx: int) -> LisaCatalog:
        """Returns a given catalog by its number in the list of LISA catalogs

        Args:
            idx (int): index of the catalog to retrieve

        Returns:
            LisaCatalog: the Lisa catalog
        """
        location = self.metadata.iloc[idx]["location"]
        name = self.metadata.index[idx]
        return LisaCatalog(name, location)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_catalog_by_name(self, name: str) -> LisaCatalog:
        """Returns a given catalog by its name.

        Args:
            name (str): name of the catalog to retrieve

        Returns:
            LisaCatalog: the Lisa catalog
        """
        cat_idx = self.metadata.index.get_loc(name)
        return self.get_catalog(cat_idx)

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_lineage(self, cat_name: str, src_name: str) -> pd.DataFrame:
        """Returns a time-dependent catalog for the evolution of a particular
        source in a series of catalogs.

        Args:
            cat_name (str): catalog from which the lineage starts
            src_name (str): particular source

        Returns:
            pd.DataFrame: a time-dependent catalog for the evolution of a particular source in a series of catalogs
        """
        dfs = list()
        while src_name != "" and cat_name not in [None, ""]:
            detections = self.get_catalog_by_name(cat_name).get_dataset("detections")
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
        histDF.drop_duplicates(subset="Log Likelihood", keep="last", inplace=True)
        histDF.sort_values(by="Observation Week", ascending=True, inplace=True)
        return histDF

    @UtilsMonitoring.io(level=logging.TRACE)
    def get_lineage_data(self, lineage: pd.DataFrame) -> pd.DataFrame:
        """Returns the merge of all of the different epochs of obervation for the evolution of a particular source in a series of catalogs

        Args:
            lineage (pd.DataFrame): a time-dependent catalog for the evolution of a particular source in a series of catalogs

        Returns:
            pd.DataFrame: a time-dependent catalog for the evolution of a particular source in a series of catalogs seen at different epochs
        """

        def _process_lineage(source_epoch, source_data, obs_week):
            source_data.insert(len(source_data.columns), "Source", source_epoch, True)
            source_data.insert(
                len(source_data.columns), "Observation Week", obs_week, True
            )
            return source_data

        source_epochs = list(lineage.index)

        merge_source_epochs = pd.concat(
            [
                _process_lineage(
                    source_epoch,
                    self.get_catalog_by_name(
                        lineage.loc[source_epoch]["Catalog"]
                    ).get_dataset(f"{source_epoch}_chain"),
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
