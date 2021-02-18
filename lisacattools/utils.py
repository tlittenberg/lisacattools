from astropy.coordinates.builtin_frames import ecliptic
import pandas as pd
import matplotlib.transforms as transforms
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import healpy as hp
from enum import Enum


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


def HPbin(df, nside, system: FrameEnum = FrameEnum.GALACTIC):
    # Assigns each lat/lon coordinate to a HEALPPIX Bin. Optional argument 'system' can be 'FrameEnum.GALACTIC' [default] or 'Ecliptic'

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
            f"{system} ({type(system)}) is not a valid coordinate system, please choose FrameEnum.GALACTIC or FrameEnum.ECLIPTIC"
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


def convert_ecliptic_to_galactic(data: pd.DataFrame):
    lamb = None
    try:
        lamb = (
            data["Ecliptic Longitude"]
            if "Ecliptic Longitude" in data.columns
            else data["ecliptic longitude"]
        )
    except:
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
    except:
        try:
            beta = (
                np.pi / 2 - np.arccos(np.array(data["coslat"]))
                if "cos ecliptic colatitude" in data.columns
                or "coslat" in data.columns
                else np.pi / 2
                - np.arccos(np.array(data["cos ecliptic colatitude"]))
            )
        except:
            raise Exception(
                "ERROR: Unable to find ecliptic latitude in data frame"
            )

    ecliptic_coord = SkyCoord(
        lamb * u.rad, beta * u.rad, frame="barycentrictrueecliptic"
    )
    galactic_coord = ecliptic_coord.galactic
    l = galactic_coord.l
    b = galactic_coord.b

    if not ("Galactic Latitude" in data.columns):
        data.insert(len(data.columns), "Galactic Longitude", l, True)
        data.insert(len(data.columns), "Galactic Latitude", b, True)
    else:
        data["Galactic Longitude"] = l
        data["Galactic Latitude"] = b
    return
