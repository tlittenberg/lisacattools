# -*- coding: utf-8 -*-
# lisacattools - A small example package for using LISA catalogs
# Copyright (C) 2020 - 2025 - James I. Thorpe, Tyson B. Littenberg, Jean-Christophe Malapert
# This file is part of lisacattools <https://github.com/tlittenberg/lisacattools>
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from functools import partial
from functools import wraps
from typing import List
from typing import Union
from typing import Callable
from loguru import logger

import healpy as hp
import matplotlib.transforms as transforms
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord
from matplotlib.patches import Ellipse

from .monitoring import UtilsMonitoring, LogLevel


class DocEnum(Enum):
    """Enum where we can add documentation."""

    def __new__(cls, value, doc=None):
        # calling super().__new__(value) here would fail
        self = object.__new__(cls)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self


class FrameEnum(DocEnum):
    """Supported reference frame"""

    GALACTIC = "Galactic", "Galactic frame"
    ECLIPTIC = "Ecliptic", "Ecliptic frame"


class CacheManager:
    memory_cache = {}

    @staticmethod
    def get_cache_pandas(
        func: Callable = None,
        keycache_argument: Union[int, List[int]] = 0,
        level: str = "INFO",  # loguru accepts string levels like "DEBUG", "INFO", etc.
    ):
        """Cache a pandas DataFrame in memory.

        Parameters
        ----------
        func : Callable, optional
            Function to cache (default: None)
        keycache_argument : int or list of int
            Argument index(es) used as cache key (default: 0)
        level : str
            Log level for messages (default: "INFO")

        Returns
        -------
        Callable
            Wrapped function with caching
        """
        if func is None:
            return partial(
                CacheManager.get_cache_pandas,
                keycache_argument=keycache_argument,
                level=level,
            )

        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(keycache_argument, int):
                indices = [keycache_argument]
            else:
                indices = keycache_argument

            # Check validity of indices
            if any(i >= len(args) for i in indices):
                logger.warning(
                    f"[{func.__name__}] Invalid keycache_argument index: {indices}, args: {len(args)}"
                )
                return func(*args, **kwargs)

            # Create cache key
            try:
                key = "-".join(str(args[i]) for i in indices)
            except Exception as e:
                logger.warning(f"[{func.__name__}] Failed to build cache key: {e}")
                return func(*args, **kwargs)

            # Return from cache if available
            if key in CacheManager.memory_cache:
                logger.log(level, f"[{func.__name__}] Retrieved result from cache for key: {key}")
                return CacheManager.memory_cache[key].copy()

            # Compute and cache the result
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                CacheManager.memory_cache.clear()  # Reset cache (only one key allowed)
                CacheManager.memory_cache[key] = result.copy()
                logger.log(level, f"[{func.__name__}] Cached result for key: {key}")
            else:
                logger.warning(f"[{func.__name__}] Result is not a DataFrame, not cached.")

            return result

        return wrapper


def HPbin(df, nside, system: FrameEnum = FrameEnum.GALACTIC):
    # Assigns each lat/lon coordinate to a HEALPPIX Bin. Optional argument
    # 'system' can be 'FrameEnum.GALACTIC' [default] or 'Ecliptic'

    # load in the coordinates in radians
    if system == FrameEnum.GALACTIC:
        if not ("Galactic Latitude" in df.columns):
            convert_ecliptic_to_galactic(df)

        lat = np.deg2rad(np.array(df["Galactic Latitude"]))
        lon = np.deg2rad(np.array(df["Galactic Longitude"]))
    elif system == FrameEnum.ECLIPTIC:
        lat = np.array(df["Ecliptic Latitude"])
        lon = np.array(df["Ecliptic Longitude"])
    else:
        raise Exception(
            f"{system} ({type(system)}) is not a valid coordinate system, \
                please choose FrameEnum.GALACTIC or FrameEnum.ECLIPTIC"
        )
        return

    # make the healpix map and insert into the passed dataframe
    # the latitude/co-latitude convention in HEALPY
    hpidx = hp.ang2pix(nside, np.pi / 2.0 - lat, lon)
    if not ("HEALPix bin" in df.columns):
        df.insert(len(df.columns), "HEALPix bin", hpidx, True)
    else:
        df["HEALPix bin"] = hpidx
    return


@UtilsMonitoring.time_spent(level=LogLevel.DEBUG)
def HPhist(source, nside, system: FrameEnum = FrameEnum.GALACTIC):

    HPbin(source, nside, system)

    # make an empty array for all the bins
    npix = hp.nside2npix(nside)
    hp_map = np.zeros(npix, dtype=int)
    # count samples in the non-empty bins
    hp_idx, hp_cnts = np.unique(source["HEALPix bin"], return_counts=True)
    # fill in the non-empty bins
    hp_map[hp_idx] = hp_cnts
    return hp_map


@UtilsMonitoring.time_spent(level=LogLevel.DEBUG)
def convert_galactic_to_cartesian(
    data: pd.DataFrame, long_name, lat_name, distance_name
):
    longitude = data[long_name].to_list()
    latitude = data[lat_name].to_list()
    distance = data[distance_name].to_list()
    galactic_coord = SkyCoord(
        longitude * u.degree,
        latitude * u.degree,
        frame="galactic",
        distance=distance,
    )
    cartesian = galactic_coord.cartesian
    data["X"] = cartesian.x
    data["Y"] = cartesian.y
    data["Z"] = cartesian.z


@UtilsMonitoring.time_spent(level=LogLevel.DEBUG)
def convert_ecliptic_to_galactic(data: pd.DataFrame):
    lamb = None
    try:
        lamb = (
            data["Ecliptic Longitude"]
            if "Ecliptic Longitude" in data.columns
            else data["ecliptic longitude"]
        )
    except:  # noqa: E722
        raise Exception(
            "ERROR: Unable to find ecliptic longitude in data frame"
        )
    lamb = lamb.to_list()
    try:
        beta = (
            data["Ecliptic Latitude"]
            if "Ecliptic Latitude" in data.columns
            else data["ecliptic latitude"]
        )
        beta = beta.to_list()
    except:  # noqa: E722
        try:
            beta = (
                np.pi / 2 - np.arccos(np.array(data["coslat"]))
                if "cos ecliptic colatitude" in data.columns
                or "coslat" in data.columns
                else np.pi / 2
                - np.arccos(np.array(data["cos ecliptic colatitude"]))
            )
        except:  # noqa: E722
            raise Exception(
                "ERROR: Unable to find ecliptic latitude in data frame"
            )
    ecliptic_coord = SkyCoord(
        lamb * u.rad, beta * u.rad, frame="barycentrictrueecliptic"
    )
    galactic_coord = ecliptic_coord.galactic
    gal_longitude = galactic_coord.l
    gal_latitude = galactic_coord.b
    # gal_latitude.wrap_angle = 180 * u.deg
    gal_longitude.wrap_angle = 180 * u.deg
    if not ("Galactic Latitude" in data.columns):
        data.insert(
            len(data.columns),
            "Galactic Longitude",
            gal_longitude.to_value(),
            True,
        )
        data.insert(
            len(data.columns),
            "Galactic Latitude",
            gal_latitude.to_value(),
            True,
        )
    else:
        data["Galactic Longitude"] = gal_longitude
        data["Galactic Latitude"] = gal_latitude
    return


def getSciRD(f, Tobs):
    # Compute the LISA Sensitivity curve given a set of Fourier frequencies
    # and an observation time
    # Curve is in units of strain amplitude and is defined by SciRD available
    # at: https://www.cosmos.esa.int/documents/678316/1700384/SciRD.pdf

    f1 = np.array(0.4 * 1e-3)
    f2 = np.array(25 * 1e-3)
    R = 1 + np.power((f / f2), 2)
    S2 = 2.6 * 1e-41
    S1 = 5.76 * 1e-48 * (1 + np.power((f1 / f), 2))
    Sh = (1 / 2) * (20 / 3) * (S1 / (np.power((2 * np.pi * f), 4)) + S2) * R
    Sha = np.sqrt(Sh / Tobs)
    return Sha


def get_DL(df):
    # Estimate luminosity distance (in kpc) from GW amplitude, frequency, and
    # frequency derivative
    c = 2.99e8  # speed of light in m/s
    kpc2m = 3.086e19  # 1 kiloparsec in meters
    r = (
        (5 / (96 * (np.pi**2)))
        * (c / df["Amplitude"])
        * (df["Frequency Derivative"])
        / np.power(df["Frequency"], 3)
        * (1 / kpc2m)
    )
    df.insert(len(df.columns), "Luminosity Distance", r, True)
    return


def get_Mchirp(df):
    TSUN = 4.9169e-6  # Mass of the Sun \f$M_\odot G c^{-3}\f$ [s]
    Mc = (
        np.power(
            df["Frequency Derivative"]
            / (96.0 / 5.0)
            / np.power(np.pi, 8.0 / 3.0)
            / np.power(df["Frequency"], 11.0 / 3.0),
            3.0 / 5.0,
        )
        / TSUN
    )
    df.insert(len(df.columns), "Chirp Mass", Mc, True)
    return


# ellipse_area
def ellipse_area(df):
    # Compute 90% ellipse area from chain samples
    cov = np.array(df.cov())
    ev = np.linalg.eigvals(cov)
    ax = 2.0 * np.sqrt(
        4.605 * ev
    )  # the 4.605 corresponds to 90%, for 95% we'd use 5.991
    return np.pi * ax[0] * ax[1]


# confidence_ellipse
@UtilsMonitoring.time_spent(level=LogLevel.DEBUG)
def confidence_ellipse(df, ax, n_std=1.0, facecolor="none", **kwargs):
    # Plot an error ellipse on some axes. It takes a 2D data frame of
    # parameters as its input
    mean = np.array(df.mean())

    cov = np.array(df.cov())
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse(
        (0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs,
    )

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std

    transf = (
        transforms.Affine2D()
        .rotate_deg(45)
        .scale(scale_x, scale_y)
        .translate(mean[0], mean[1])
    )

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)
