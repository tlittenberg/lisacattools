# -*- coding: utf-8 -*-
# Copyright 2021 James I. Thorpe, Tyson B. Littenberg, Jean-Christophe Malapert
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import logging.config
import os

from ._version import __author__  # noqa: F401
from ._version import __author_email__  # noqa: F401
from ._version import __copyright__  # noqa: F401
from ._version import __description__  # noqa: F401
from ._version import __license__  # noqa: F401
from ._version import __name__  # noqa: F401
from ._version import __title__  # noqa: F401
from ._version import __url__  # noqa: F401
from ._version import __version__  # noqa: F401
from .analyze import CatalogAnalysis
from .analyze import HistoryAnalysis
from .analyze import LisaAnalyse
from .catalog import GWCatalog
from .catalog import GWCatalogs
from .catalog import GWCatalogType
from .custom_logging import LogRecord
from .custom_logging import UtilsLogs
from .utils import confidence_ellipse
from .utils import convert_ecliptic_to_galactic
from .utils import convert_galactic_to_cartesian
from .utils import ellipse_area
from .utils import FrameEnum
from .utils import get_DL
from .utils import get_Mchirp
from .utils import getSciRD
from .utils import HPhist

logging.getLogger(__name__).addHandler(logging.NullHandler())

UtilsLogs.addLoggingLevel("TRACE", 15)
try:
    PATH_TO_CONF = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(
        os.path.join(PATH_TO_CONF, "logging.conf"),
        disable_existing_loggers=False,
    )
    logging.debug(
        "file %s loaded" % os.path.join(PATH_TO_CONF, "logging.conf")
    )
except Exception as exception:  # pylint: disable=broad-except
    logging.warning("cannot load logging.conf : %s" % exception)
logging.setLogRecordFactory(LogRecord)  # pylint: disable=no-member

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
TRACE = 15
INFO = 20
DEBUG = 10
NOTSET = 0
OFF = 100

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
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "TRACE",
    "INFO",
    "DEBUG",
    "NOTSET",
    "OFF",
]
