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

"""This module is the interface for gravitational wavelength catalogs. It is
responsible for :
- register new catalog implementations as plugins
- loading detections and source sample
"""

from abc import ABC, abstractmethod

from typing import List, Union
import importlib

import pandas as pd

from dataclasses import dataclass

from .monitoring import UtilsMonitoring

from .custom_logging import UtilsLogs


@dataclass
class GWCatalogPlugin:
    """Store information to load a plugin implementing the GW catalog.

    The different information are:
    - the module name
    - the class name
    """

    module_name: str
    class_name: str


class GWCatalogType:
    """GW catalog implementation.

    New implementations can be added by adding an attribute using the register
    method of the GWCatalogs class.
    """

    LISA = GWCatalogPlugin("lisacattools.plugins.mbh", "LisaCatalogs")
    UCB = GWCatalogPlugin("lisacattools.plugins.ucb", "UcbCatalogs")


class GWCatalog:
    """Interface for handling a GW catalog."""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "name")
            and callable(subclass.name)
            and hasattr(subclass, "location")
            and callable(subclass.location)
            and hasattr(subclass, "get_detections")
            and callable(subclass.get_detections)
            and hasattr(subclass, "get_attr_detections")
            and callable(subclass.get_attr_detections)
            and hasattr(subclass, "get_median_source")
            and callable(subclass.get_median_source)
            and hasattr(subclass, "get_source_sample")
            and callable(subclass.get_source_sample)
            and hasattr(subclass, "get_attr_source_sample")
            and callable(subclass.get_source_sample)
            and hasattr(subclass, "describe_source_sample")
            and callable(subclass.describe_source_sample)
            or NotImplemented
        )

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the GW catalog.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            str: name of the GW catalog
        """
        raise NotImplementedError("Not implemented")

    @property
    @abstractmethod
    def location(self) -> str:
        """Returns the location of the GW catalog.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            str: the location of the GW catalog
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_detections(
        self, attr: List[str] = None
    ) -> Union[List[str], pd.DataFrame]:
        """Returns the GW detections.

        When no argument is provided, the name of each detection is returned
        When arguments are provided, each detection is returned with the attributes.

        Args:
            attr (List[str], optional): List of attributes. Defaults to None.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Union[List[str], pd.DataFrame]: the name of each detection or the asked attributed of each detection
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_attr_detections(self) -> List[str]:
        """Returns the attributes of the detections catalog.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            List[str]: the list of attributes
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_median_source(self, attr: str) -> pd.DataFrame:
        """Returns the source for which the median is computed on the attribute.

        Args:
            attr (str): attribute name

        Raises:
            NotImplementedError: Not implemented

        Returns:
            pd.DataFrame: the source for which the median is computed on the attribute
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_source_sample(
        self, source_name: str, attr: List[str]
    ) -> pd.DataFrame:
        """Returns the sample of the source

        Args:
            source_name (str): source name
            attr (List[str]): the list of attributes to return in the result

        Raises:
            NotImplementedError: [description]

        Returns:
            pd.DataFrame: the samples of the source
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_attr_source_sample(self, source_name: str) -> List[str]:
        """Returns the attributes of the source sample catalog

        Args:
            source_name (str): source name

        Raises:
            NotImplementedError: Not implemented

        Returns:
            List[str]: the attributes
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def describe_source_sample(self, source_name: str) -> pd.DataFrame:
        """Give some statisctics about the source sample

        Args:
            source_name (str): source name

        Raises:
            NotImplementedError: Not implemented

        Returns:
            pd.DataFrame: statistics
        """
        raise NotImplementedError("Not implemented")


class GWCatalogs(ABC):
    """Interface fo handling GW catalogs over the time"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "metadata")
            and callable(subclass.metadata)
            and hasattr(subclass, "count")
            and callable(subclass.count)
            and hasattr(subclass, "get_catalogs_name")
            and callable(subclass.get_catalogs_name)
            and hasattr(subclass, "get_first_catalog")
            and callable(subclass.get_first_catalog)
            and hasattr(subclass, "get_last_catalog")
            and callable(subclass.get_last_catalog)
            and hasattr(subclass, "get_catalog")
            and callable(subclass.get_catalog)
            and hasattr(subclass, "get_catalog_by")
            and callable(subclass.get_catalog_by)
            and hasattr(subclass, "get_lineage")
            and callable(subclass.get_lineage)
            and hasattr(subclass, "get_lineage_data")
            and callable(subclass.get_lineage_data)
            or NotImplemented
        )

    @staticmethod
    def register(type: str, nodule_name: str, class_name: str):
        """Register a new implementation of GWCatalogs

        Args:
            type (str): name of the implementation
            nodule_name (str): nodule name where the implementation is done
            class_name (str): class name of the implementation
        """
        setattr(
            GWCatalogType, str(type), GWCatalogPlugin(nodule_name, class_name)
        )

    @staticmethod
    def create(
        type: GWCatalogPlugin, directory: str, pattern: str
    ) -> "GWCatalogs":
        """Create a new object for handling a set of specific catalogs.

        Returns:
            GWCatalogs: the object implementing a set of specific catalogs
        """
        module = importlib.import_module(type.module_name)
        my_class = getattr(module, type.class_name)
        return my_class(directory, pattern)

    @property
    @abstractmethod
    def metadata(self) -> pd.DataFrame:
        """metadata.

        :getter: Returns the metadata of the catalog set
        :type: pd.DataFrame
        """
        raise NotImplementedError("Not implemented")

    @property
    @abstractmethod
    def count(self) -> int:
        """Count the number of catalogs in the catalog set.

        :getter: Returns the number of catalogs in the catalog set
        :type: int
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_catalogs_name(self) -> List[str]:
        """Returns the name of each catalog included in the catalog set

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            List[str]: name of each catalog
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_first_catalog(self) -> GWCatalog:
        """Returns the first catalog from catalog set

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            GWCatalog: the fist catalog
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_last_catalog(self) -> GWCatalog:
        """Returns the last catalog from the catalog set.

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            GWCatalog: the last catalog
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_catalog(self, idx: int) -> GWCatalog:
        """Returns a catalog based on its position in the catalog set

        Args:
            idx (int): position of the catalog (first idx: 0)

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            GWCatalog: catalog
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_catalog_by(self, name: str) -> GWCatalog:
        """Returns a catalog based on its name in the catalog set

        Args:
            name (str): name of the catalog

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            GWCatalog: the catalog
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_lineage(self, cat_name: str, src_name: str) -> pd.DataFrame:
        """Returns a time-dependent catalog for the evolution of a particular
        source in a series of catalogs.

        Args:
            cat_name (str): catalog from which the lineage starts
            src_name (str): particular source

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            pd.DataFrame: a time-dependent catalog for the evolution of a particular source in a series of catalogs
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_lineage_data(self, lineage: pd.DataFrame) -> pd.DataFrame:
        """Returns the merge of all of the different epochs of obervation for the evolution of a particular source in a series of catalogs

        Args:
            lineage (pd.DataFrame): a time-dependent catalog for the evolution of a particular source in a series of catalogs

        Raises:
            NotImplementedError: When the method is not implemented

        Returns:
            pd.DataFrame: a time-dependent catalog for the evolution of a particular source in a series of catalogs seen at different epochs
        """
        raise NotImplementedError("Not implemented")
