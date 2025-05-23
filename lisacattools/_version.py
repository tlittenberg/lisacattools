# -*- coding: utf-8 -*-
# lisacattools - A small example package for using LISA catalogs
# Copyright (C) 2020 - 2025 - James I. Thorpe, Tyson B. Littenberg, Jean-Christophe Malapert
# This file is part of lisacattools <https://github.com/tlittenberg/lisacattools>
# SPDX-License-Identifier: Apache-2.0

"""Project metadata."""
from importlib.metadata import metadata

pkg_metadata = metadata("lisacattools")

__name__ = pkg_metadata.get("name", "unknown")
__version__ = pkg_metadata.get("version", "0.0.0")
__title__ = pkg_metadata.get("name", "unknown")
__description__ = pkg_metadata.get("summary", "")
__url__ = pkg_metadata.get("homepage", "")
__author__ = pkg_metadata.get("author", "unknown")
__author_email__ = pkg_metadata.get("author-email", "unknown")
__license__ = pkg_metadata.get("license", "Unknown")
__copyright__ = "2020, James I. Thorpe, Tyson B. Littenberg, Jean-Christophe Malapert"

