# -*- coding: utf-8 -*-
# lisacattools - A small example package for using LISA catalogs
# Copyright (C) 2020 - 2025 - James I. Thorpe, Tyson B. Littenberg, Jean-Christophe Malapert
# This file is part of lisacattools <https://github.com/tlittenberg/lisacattools>
# SPDX-License-Identifier: Apache-2.0

from loguru import logger
import sys

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
from .utils import confidence_ellipse
from .utils import convert_ecliptic_to_galactic
from .utils import convert_galactic_to_cartesian
from .utils import ellipse_area
from .utils import FrameEnum
from .utils import get_DL
from .utils import get_Mchirp
from .utils import getSciRD
from .utils import HPhist
from .monitoring import LogLevel

logger.remove()
logger.add(sys.stdout, level=LogLevel.INFO)

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
    "HPhist"
]
