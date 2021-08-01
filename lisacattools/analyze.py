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
import logging
import os
from typing import Dict
from typing import List
from typing import NoReturn

import corner
import ligo.skymap.plot  # noqa: F401
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .catalog import GWCatalog
from .catalog import GWCatalogs
from .custom_logging import UtilsLogs
from .monitoring import UtilsMonitoring
from .utils import FrameEnum
from .utils import HPhist

UtilsLogs.addLoggingLevel("TRACE", 15)


class LisaAnalyse:
    """Factory to create an analysis for a catalog or a time-evolution of the
    catalog."""

    @staticmethod
    def create(catalog, save_dir=None):
        obj = None
        if isinstance(catalog, GWCatalog):
            obj = CatalogAnalysis(catalog, save_dir)
        elif isinstance(catalog, GWCatalogs):
            obj = HistoryAnalysis(catalog, save_dir)
        else:
            raise NotImplementedError(f"type {type(catalog)} not implemented")
        return obj


class AbstractLisaAnalyze:
    """Abstract Object to link the two implementation and to share some
    method."""

    def __init__(self):
        pass

    @UtilsMonitoring.io(level=logging.DEBUG)
    def _get_variable(
        self, dico: Dict, variable: str, default_val: object
    ) -> object:
        return default_val if variable not in dico else dico[variable]

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_corners_ds(self, sources, *args, **kwargs):
        color = self._get_variable(kwargs, "color", "red")
        plot_datapoints = self._get_variable(kwargs, "plot_datapoints", False)
        fill_contours = self._get_variable(kwargs, "fill_contours", True)
        bins = self._get_variable(kwargs, "bins", 50)
        smooth = self._get_variable(kwargs, "smooth", 1.0)
        levels = self._get_variable(kwargs, "levels", [0.68, 0.95])
        fontsize = self._get_variable(kwargs, "fontsize", 16)
        fig = self._get_variable(kwargs, "fig", None)
        title = self._get_variable(kwargs, "title", "parameters")
        if fig:
            corner.corner(
                sources,
                fig=fig,
                color=color,
                plot_datapoints=plot_datapoints,
                fill_contours=fill_contours,
                bins=bins,
                smooth=smooth,
                levels=levels,
                label_kwargs={"fontsize": fontsize},
            )
        else:
            figIn = corner.corner(
                sources,
                color=color,
                plot_datapoints=plot_datapoints,
                fill_contours=fill_contours,
                bins=bins,
                smooth=smooth,
                levels=levels,
                label_kwargs={"fontsize": fontsize},
            )
            figIn.suptitle(title)


class CatalogAnalysis(AbstractLisaAnalyze):
    """Handle the analysis of one catalog."""

    def __init__(self, catalog: GWCatalog, save_img_dir=None):
        """Init the analysis with a Lisa catalog."""
        self.catalog = catalog
        self.save_img_dir = save_img_dir

    @property
    def catalog(self):
        """Catalog.

        :getter: Returns the catalog of this analysis
        :setter: Sets the catalog.
        :type: GWCatalog
        """
        return self._catalog

    @catalog.setter
    def catalog(self, value):
        self._catalog = value

    @property
    def save_img_dir(self):
        """Save image directory for plot.

        :getter: Returns the directory where plots are saved
        :setter: Sets the directory where plots are saved.
        :type: str
        """
        return self._save_img_dir

    @save_img_dir.setter
    def save_img_dir(self, value):
        self._save_img_dir = value

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_mbh_mergers_history(self) -> NoReturn:
        """Plot the history of observed mergers."""

        mergeTimes = self.catalog.get_detections("Barycenter Merge Time")
        mergeTimes.sort_values(ascending=True, inplace=True)
        mergeT = np.insert(np.array(mergeTimes) / 86400, 0, 0)
        mergeCount = np.arange(0, len(mergeTimes) + 1)
        fig, ax = plt.subplots(figsize=[8, 6], dpi=100)
        ax.step(mergeT, mergeCount, where="post")
        for m in range(0, len(mergeTimes)):
            plt.annotate(
                mergeTimes.index[m],  # this is the text
                # this is the point to label
                (mergeTimes[m] / 86400, mergeCount[m]),
                textcoords="offset points",  # how to position the text
                xytext=(2, 5),  # distance from text to points (x,y)
                rotation="horizontal",
                ha="left",
            )  # horizontal alignment can be left, right or center
        ax.set_xlabel("Observation Time [days]")
        ax.set_ylabel("Merger Count")
        ax.set_title(f"MBH Mergers in catalog {self.catalog.name}")
        ax.grid()
        if self.save_img_dir:
            fig.savefig(
                os.path.join(
                    self.save_img_dir,
                    "MBH_mergers_" + self.catalog.name + ".png",
                )
            )
        # plt.show()

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_individual_sources(self) -> NoReturn:
        """Plot the indivual sources."""

        fig, ax = plt.subplots(figsize=[8, 6], dpi=100)
        detections = self.catalog.get_detections(["Mass 1", "Mass 2"])
        sources = list(detections.index)
        for idx, source in enumerate(sources):
            chain = self.catalog.get_source_samples(
                source, ["Mass 1", "Mass 2"]
            )
            l1, m1, h1 = np.quantile(
                np.array(chain["Mass 1"]), [0.05, 0.5, 0.95]
            )
            l2, m2, h2 = np.quantile(
                np.array(chain["Mass 2"]), [0.05, 0.5, 0.95]
            )
            if idx < 10:
                mkr = "o"
            else:
                mkr = "^"
            ax.errorbar(
                m1,
                m2,
                xerr=np.vstack((m1 - l1, h1 - m1)),
                yerr=np.vstack((m2 - l2, h2 - m2)),
                label=source,
                markersize=6,
                capsize=2,
                marker=mkr,
                markerfacecolor="none",
            )
        ax.set_xscale("log", nonpositive="clip")
        ax.set_yscale("log", nonpositive="clip")
        ax.grid()
        ax.set_xlabel("Mass 1 [MSun]")
        ax.set_ylabel("Mass 2 [MSun]")
        ax.set_title("90%% CI for Component Masses in %s " % self.catalog.name)
        ax.legend(loc="lower right")
        if self.save_img_dir:
            fig.savefig(
                os.path.join(
                    self.save_img_dir,
                    "component_masses" + self.catalog.name + ".png",
                )
            )
        # plt.show()

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_corners(self, source_name, params, *args, **kwargs) -> NoReturn:
        """Some corners plots."""
        sources = self.catalog.get_source_samples(source_name, params)
        self.plot_corners_ds(source_name, sources, *args, **kwargs)

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_skymap(
        self, source, nside, system: FrameEnum = FrameEnum.ECLIPTIC
    ) -> NoReturn:
        """Plot skymap."""
        hp_map = HPhist(source, nside, system)
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = plt.axes(
            [0.05, 0.05, 0.9, 0.9], projection="geo degrees mollweide"
        )
        ax.grid()
        ax.imshow_hpx((hp_map), cmap="plasma")
        if self.save_img_dir:
            fig.savefig(os.path.join(self.save_img_dir, "skymap.png"))


class HistoryAnalysis(AbstractLisaAnalyze):
    """Analyse a particular source to see how it's parameter estimates
    improve over time"""

    def __init__(self, catalogs: GWCatalogs, save_img_dir=None):
        """Init the HistoryAnalysis with all catalogs to load the parameter
        estimates over the time."""
        self.catalogs = catalogs
        self.save_img_dir = save_img_dir

    @property
    def catalogs(self):
        """Catalogs.

        :getter: Returns the catalogs of this analysis
        :setter: Sets the catalogs.
        :type: GWCatalogs
        """
        return self._catalogs

    @catalogs.setter
    def catalogs(self, value):
        self._catalogs = value

    @property
    def save_img_dir(self):
        """Save image directory for plot.

        :getter: Returns the directory where plots are saved
        :setter: Sets the directory where plots are saved.
        :type: str
        """
        return self._save_img_dir

    @save_img_dir.setter
    def save_img_dir(self, value):
        self._save_img_dir = value

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_parameter_time_evolution(
        self,
        df: pd.DataFrame,
        time_parameter: str,
        parameter: str,
        *args,
        **kwargs,
    ) -> NoReturn:
        """Plot the parameter that evolves over time.

        Note: extra parameter can be configured:
        - plot_type, default : scatter
        - grid, default : True
        - marker, default : 's'
        - linestyle, default : '-'
        - yscale, default : log
        - title, default : Evolution

        Args:
            df (pd.DataFrame): data
            time_parameter (str): time parameter in the data
            parameter (str): parameter to plot over the time
        """
        plot_type = self._get_variable(kwargs, "scatter", "scatter")
        grid = self._get_variable(kwargs, "grid", True)
        marker = self._get_variable(kwargs, "marker", "s")
        linestyle = self._get_variable(kwargs, "linestyle", "-")
        yscale = self._get_variable(kwargs, "yscale", "log")
        title: str = self._get_variable(kwargs, "title", "Evolution")

        fig, ax = plt.subplots(figsize=[8, 6], dpi=100)
        df.plot(
            kind=plot_type,
            x=time_parameter,
            y=parameter,
            ax=ax,
            grid=grid,
            marker=marker,
            linestyle=linestyle,
        )
        ax.set_yscale(yscale)
        ax.set_title(title)
        if self.save_img_dir:
            fig.savefig(
                os.path.join(
                    self.save_img_dir, title.replace(" ", "_") + ".png"
                )
            )

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_parameter_time_evolution_from_source(
        self,
        catalog_name: str,
        source_name: str,
        time_parameter: str,
        parameter: str,
        *args,
        **kwargs,
    ) -> NoReturn:
        """Plot the parameter that evolves over time for a given source
        starting from a catalog.

        Note: extra parameter can be configured:
        - plot_type, default : scatter
        - grid, default : True
        - marker, default : 's'
        - linestyle, default : '-'
        - yscale, default : log
        - title, default : Evolution

        Args:
            df (pd.DataFrame): data
            catalog_name (str) : Start the evolution from the oldest one
            until that one
            source_name (str) : source name to follow up
            time_parameter (str): time parameter in the data
            parameter (str): parameter to plot over the time
        """
        catalogs = self.catalogs
        srcHist = catalogs.get_lineage(catalog_name, source_name)
        self.plot_parameter_time_evolution(
            srcHist, time_parameter, parameter, *args, **kwargs
        )

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_parameters_evolution(
        self,
        all_epochs: pd.DataFrame,
        params: List,
        scales: List,
        *args,
        **kwargs,
    ) -> NoReturn:
        """Show evolution over many different epochs.

        Args:
            all_epochs (pd.DataFrame): observation of a source at
            different epochs
            params (List): list of parameters to plot
            scales (List): Scale for each plot
        """
        title = self._get_variable(kwargs, "title", "Parameter Evolution")
        x_title = self._get_variable(kwargs, "x_title", "Observation Week")
        nrows = int(np.ceil(len(params) / 2))
        fig = plt.figure(figsize=(10.0, 10.0), dpi=100)

        for idx, param in enumerate(params):
            ax = fig.add_subplot(nrows, 2, idx + 1)
            sns.violinplot(
                ax=ax,
                x=x_title,
                y=param,
                data=all_epochs,
                scale="width",
                width=0.8,
                inner="quartile",
            )
            ax.set_yscale(scales[idx])
            ax.grid(axis="y")

        fig.suptitle(title)
        if self.save_img_dir:
            fig.savefig(
                os.path.join(
                    self.save_img_dir, title.replace(" ", "_") + ".png"
                )
            )

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_parameters_correlation_evolution(
        self,
        allEpochs: pd.DataFrame,
        wks: List,
        params: List,
        colors: List,
        *args,
        **kwargs,
    ) -> NoReturn:
        """To dig into how parameter correlations might change over time, we
        can look at a time-evolving corner plot

        Args:
            allEpochs (pd.DataFrame): observation of a source at different
            epochs
            wks (List): weeks to plot
            params (List): parameters to plot
            colors (List): color according the weeks
        """
        title = self._get_variable(kwargs, "title", "Evolution of parameters")
        fig = plt.figure(figsize=[8, 8], dpi=100)
        for idx, wk in enumerate(wks):
            epoch = allEpochs[allEpochs["Observation Week"] == wk]
            self.plot_corners_ds(epoch[params], fig=fig, color=colors[idx])
        fig.suptitle(title)
        if self.save_img_dir:
            fig.savefig(
                os.path.join(
                    self.save_img_dir, title.replace(" ", "_") + ".png"
                )
            )

    @UtilsMonitoring.io(entry=True, exit=False, level=logging.DEBUG)
    def plot_skymap_evolution(
        self,
        nside: int,
        allEpochs: pd.DataFrame,
        wks: List,
        system: FrameEnum = FrameEnum.GALACTIC,
        *args,
        **kwargs,
    ) -> NoReturn:
        """Plot the skymap evolution

        Args:
            nside (int): parameter for healpix related to the number of cells
            allEpochs (pd.DataFrame): observation of a source at different
            epochs
            wks (List): weeks to plot
            system (FrameEnum, optional): coordinate reference frame. Defaults
            to 'FrameEnum.GALACTIC'.
        """
        title = self._get_variable(
            kwargs, "title", "Sky Localization Evolution"
        )
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ncols = 2
        nrows = int(np.ceil(len(wks) / ncols))
        for idx, wk in enumerate(wks):
            hpmap = HPhist(
                allEpochs[allEpochs["Observation Week"] == wk], nside, system
            )
            ax = fig.add_subplot(
                nrows, ncols, idx + 1, projection="geo degrees mollweide"
            )
            ax.grid()
            # ax.contour_hpx(hpmap, cmap='Blues',levels=4,alpha=0.8)
            ax.imshow_hpx(hpmap, cmap="plasma")
            ax.set_title(f"Week {wk}")
        fig.suptitle(title)
        if self.save_img_dir:
            fig.savefig(
                os.path.join(
                    self.save_img_dir, title.replace(" ", "_") + ".png"
                )
            )
