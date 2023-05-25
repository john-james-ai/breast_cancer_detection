#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /cadx/data/explore/metadata.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 24th 2023 04:24:21 pm                                                 #
# Modified   : Thursday May 25th 2023 05:51:32 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from cadx.data.explore.base import CancerMeta
from cadx.services.visual.config import VisualConfig

sns.set_style(VisualConfig.style)
sns.set_palette = sns.dark_palette(VisualConfig.palette.blue, reverse=True, as_cmap=True)


# ------------------------------------------------------------------------------------------------ #
#                                      MASS ABNORMALITIES                                          #
# ------------------------------------------------------------------------------------------------ #
class MassMeta(CancerMeta):
    """Metadata for mass abnormalities.

    Args:
        filepath (str): Path to the metadata file.
        name (str): Name for the Dataset
        train (bool): Wether the dataset is the training dataset. False if it is the test set.
    """

    __name = "Masses"

    def __init__(self, train_filepath: str, test_filepath: str, name: str = None) -> None:
        self._name = name or self.__name
        super().__init__(
            train_filepath=train_filepath, test_filepath=test_filepath, name=self._name
        )

    def pathology_feature(self) -> pd.DataFrame:
        """Plots pathology vis-a-vis Mass Shape and Margins"""
        canvas = VisualConfig(figsize=(6, 4), nrows=1, ncols=2).canvas
        fig = canvas.fig
        title = f"{self._name}\nPathology by Mass Features"
        fig.suptitle(title)

        (ax1, ax2) = canvas.axs
        df1 = self.pathology_mass_shape(ax1)
        df2 = self.pathology_mass_margins(ax2)

        df1 = df1[["Pathology", "Mass Shape", "Count"]].sort_values(
            by=["Pathology", "Count"], ascending=False
        )
        df2 = df2[["Pathology", "Mass Margins", "Count"]].sort_values(
            by=["Pathology", "Count"], ascending=False
        )

        return df1, df2

    def pathology_mass_shape(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by mass_shape"""
        if not ax:
            canvas = VisualConfig(figsize=(12, 4), nrows=1, ncols=1).canvas
        ax = ax or canvas.ax

        df = pd.concat([self._train, self._test], axis=0)
        df = df.replace("BENIGN_WITHOUT_CALLBACK", "BENIGN")

        df2 = df.groupby(by=["pathology", "mass_shape"])[["patient_id"]].count().reset_index()
        df2.columns = ["Pathology", "Mass Shape", "Count"]
        df3 = df2.groupby(by=["Pathology"]).head(5).reset_index()

        ax = sns.barplot(
            x=df2["Pathology"],
            y=df2["Count"],
            hue=df2["Mass Shape"],
            ax=ax,
            saturation=0.5,
            estimator="sum",
            dodge=False,
            palette=VisualConfig.palette.blues_r,
        )
        title = "Mass Shape"
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=4, framealpha=0.3, mode="expand", ncol=2)
        plt.tight_layout()
        return df3

    def pathology_mass_margins(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by mass_margins"""
        if not ax:
            canvas = VisualConfig(figsize=(12, 4), nrows=1, ncols=1).canvas
        ax = ax or canvas.ax

        df = pd.concat([self._train, self._test], axis=0)
        df = df.replace("BENIGN_WITHOUT_CALLBACK", "BENIGN")

        df2 = df.groupby(by=["pathology", "mass_margins"])[["patient_id"]].count().reset_index()
        df2.columns = ["Pathology", "Mass Margins", "Count"]
        df3 = df2.groupby(by=["Pathology"]).head(5).reset_index()

        ax = sns.barplot(
            x=df2["Pathology"],
            y=df2["Count"],
            hue=df2["Mass Margins"],
            ax=ax,
            saturation=0.5,
            estimator="sum",
            dodge=False,
            palette=VisualConfig.palette.blues_r,
        )
        title = "Mass Margins"
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=4, framealpha=0.3, mode="expand", ncol=2)
        plt.tight_layout()
        return df3


# ------------------------------------------------------------------------------------------------ #
#                                CALCIFICATION ABNORMALITIES                                       #
# ------------------------------------------------------------------------------------------------ #
class CalcMeta(CancerMeta):
    """Metadata for calcification abnormalities.

    Args:
        filepath (str): Path to the metadata file.
        name (str): Name for the Dataset
        train (bool): Wether the dataset is the training dataset. False if it is the test set.
    """

    __name = "Calcification"

    def __init__(self, train_filepath: str, test_filepath: str, name: str = None) -> None:
        self._name = name or self.__name
        super().__init__(
            train_filepath=train_filepath, test_filepath=test_filepath, name=self._name
        )

    def pathology_feature(self) -> pd.DataFrame:
        """Plots pathology vis-a-vis Classification Type and Distribution"""
        canvas = VisualConfig(figsize=(6, 4), nrows=1, ncols=2).canvas
        fig = canvas.fig
        title = f"{self._name}\nPathology by Calcification Features"
        fig.suptitle(title)

        (ax1, ax2) = canvas.axs
        df1 = self.pathology_calc_type(ax1)
        df2 = self.pathology_calc_distribution(ax2)

        df1 = df1[["Pathology", "Calcification Type", "Count"]].sort_values(
            by=["Pathology", "Count"], ascending=False
        )
        df2 = df2[["Pathology", "Calcification Distribution", "Count"]].sort_values(
            by=["Pathology", "Count"], ascending=False
        )

        return df1, df2

    def pathology_calc_type(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by calcification type"""
        if not ax:
            canvas = VisualConfig(figsize=(12, 4), nrows=1, ncols=1).canvas
        ax = ax or canvas.ax

        df = pd.concat([self._train, self._test], axis=0)
        df = df.replace("BENIGN_WITHOUT_CALLBACK", "BENIGN")

        df2 = df.groupby(by=["pathology", "calc_type"])[["patient_id"]].count().reset_index()
        df2.columns = ["Pathology", "Calcification Type", "Count"]
        df2 = df2.groupby(by="Pathology").head(10).reset_index()
        df3 = df2.groupby(by=["Pathology"]).head(5).reset_index()

        ax = sns.barplot(
            x=df2["Pathology"],
            y=df2["Count"],
            hue=df2["Calcification Type"],
            ax=ax,
            saturation=0.5,
            estimator="sum",
            dodge=False,
            palette=VisualConfig.palette.blues_r,
        )
        title = "Calcification Type"
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=4, framealpha=0.3, mode="expand", ncol=2)
        plt.tight_layout()
        return df3

    def pathology_calc_distribution(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by calcification distribution"""
        if not ax:
            canvas = VisualConfig(figsize=(12, 4), nrows=1, ncols=1).canvas

        ax = ax or canvas.ax
        df = pd.concat([self._train, self._test], axis=0)
        df = df.replace("BENIGN_WITHOUT_CALLBACK", "BENIGN")

        df2 = (
            df.groupby(by=["pathology", "calc_distribution"])[["patient_id"]].count().reset_index()
        )
        df2.columns = ["Pathology", "Calcification Distribution", "Count"]
        df3 = df2.groupby(by=["Pathology"]).head(5).reset_index()

        ax = sns.barplot(
            x=df2["Pathology"],
            y=df2["Count"],
            hue=df2["Calcification Distribution"],
            ax=ax,
            saturation=0.5,
            estimator="sum",
            dodge=False,
            palette=VisualConfig.palette.blues_r,
        )

        title = "Calcification Distribution"
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=4, framealpha=0.3, mode="expand", ncol=2)
        plt.tight_layout()
        return df3
