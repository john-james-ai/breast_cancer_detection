#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Breast Cancer Detection from Mammography using Deep Learning                        #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/explore/metadata.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 24th 2023 04:24:21 pm                                                 #
# Modified   : Wednesday May 24th 2023 10:48:27 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import matplotlib.pyplot as plt
import seaborn as sns

from bcd.data.explore.base import CancerMeta
from bcd.services.visual.config import VisualConfig

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

    def __init__(self, train_filepath: str, test_filepath: str, name: str) -> None:
        super().__init__(train_filepath=train_filepath, test_filepath=test_filepath, name=name)

    def pathology_mass_shape(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by mass shape"""
        canvas = VisualConfig(figsize=(12, 4), nrows=2, ncols=1).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nPathology by Mass Shape"
        fig.suptitle(suptitle)

        ax1 = sns.countplot(
            y=self._train["mass shape"],
            hue=self._train["pathology"],
            ax=ax1,
            palette=VisualConfig.palette.blues_r,
        )
        ax1.get_legend().remove()
        title = "Train Set"
        ax1.set_title(title)

        ax2 = sns.countplot(
            y=self._test["mass shape"],
            hue=self._test["pathology"],
            ax=ax2,
            palette=VisualConfig.palette.blues_r,
        )
        ax2.get_legend().remove()
        title = "Test Set"
        ax2.set_title(title)

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=8)
        plt.tight_layout()

    def pathology_mass_margins(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by mass margins"""
        canvas = VisualConfig(figsize=(12, 4), nrows=2, ncols=1).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nPathology by Mass Margins"
        fig.suptitle(suptitle)

        ax1 = sns.countplot(
            y=self._train["mass margins"],
            hue=self._train["pathology"],
            ax=ax1,
            palette=VisualConfig.palette.blues_r,
        )
        ax1.get_legend().remove()
        title = "Train Set"
        ax1.set_title(title)

        ax2 = sns.countplot(
            y=self._test["mass margins"],
            hue=self._test["pathology"],
            ax=ax2,
            palette=VisualConfig.palette.blues_r,
        )
        ax2.get_legend().remove()
        title = "Test Set"
        ax2.set_title(title)

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=8)
        plt.tight_layout()


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

    def __init__(self, train_filepath: str, test_filepath: str, name: str) -> None:
        super().__init__(train_filepath=train_filepath, test_filepath=test_filepath, name=name)

    def pathology_calc_type(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by calcification type"""
        canvas = VisualConfig(figsize=(12, 8), nrows=2, ncols=1).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nPathology by Calcification Type"
        fig.suptitle(suptitle)

        ax1 = sns.countplot(
            y=self._train["calc type"],
            hue=self._train["pathology"],
            ax=ax1,
            palette=VisualConfig.palette.blues_r,
        )
        ax1.get_legend().remove()
        title = "Train Set"
        ax1.set_title(title)

        ax2 = sns.countplot(
            y=self._test["calc type"],
            hue=self._test["pathology"],
            ax=ax2,
            palette=VisualConfig.palette.blues_r,
        )
        ax2.get_legend().remove()
        title = "Test Set"
        ax2.set_title(title)

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=8)
        plt.tight_layout()

    def pathology_calc_distribution(self, ax: plt.axes = None) -> plt.axes:
        """Pathology by calcification distribution"""
        canvas = VisualConfig(figsize=(12, 4), nrows=2, ncols=1).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nPathology by Calcification Distribution"
        fig.suptitle(suptitle)

        ax1 = sns.countplot(
            y=self._train["calc distribution"],
            hue=self._train["pathology"],
            ax=ax1,
            palette=VisualConfig.palette.blues_r,
        )
        ax1.get_legend().remove()
        title = "Train Set"
        ax1.set_title(title)

        ax2 = sns.countplot(
            y=self._test["calc distribution"],
            hue=self._test["pathology"],
            ax=ax2,
            palette=VisualConfig.palette.blues_r,
        )
        ax2.get_legend().remove()
        title = "Test Set"
        ax2.set_title(title)

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=8)
        plt.tight_layout()
