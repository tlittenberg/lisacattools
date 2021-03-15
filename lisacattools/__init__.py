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

from ._version import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __name__,
    __url__,
    __version__,
)
from .utils import FrameEnum
from .analyze import LisaAnalyse, CatalogAnalysis, HistoryAnalysis
from .catalog import GWCatalogs, GWCatalog, GWCatalogType
from .utils import (
    getSciRD,
    get_DL,
    get_Mchirp,
    confidence_ellipse,
    convert_ecliptic_to_galactic,
    convert_galactic_to_cartesian,
    ellipse_area,
    HPhist,
)
import os
import logging.config
from logging import NullHandler
from .custom_logging import (
    LogRecord,
    UtilsLogs,
)

logging.getLogger(__name__).addHandler(NullHandler())

UtilsLogs.addLoggingLevel("TRACE", 15)
try:
    PATH_TO_CONF = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(os.path.join(PATH_TO_CONF, "logging.conf"))
    logging.debug("file %s loaded" % os.path.join(PATH_TO_CONF, "logging.conf"))
except Exception as exception:  # pylint: disable=broad-except
    logging.warning("cannot load logging.conf : %s" % exception)
logging.setLogRecordFactory(LogRecord)  # pylint: disable=no-member


__all__ = [
    "GWCatalogs",
    "GWCatalog",
    "GWCatalogType",
    "LisaAnalyse",
    "CatalogAnalysis",
    "HistoryAnalysis",
    "FrameEnum",
    "getSciRD",
    "get_DL",
    "get_Mchirp",
    "confidence_ellipse",
    "convert_ecliptic_to_galactic",
    "convert_galactic_to_cartesian",
    "ellipse_area",
    "HPhist",
]
