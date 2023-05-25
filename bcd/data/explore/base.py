#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Breast Cancer Detection from Mammography using Deep Learning                        #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/explore/base.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 24th 2023 03:13:32 pm                                                 #
# Modified   : Thursday May 25th 2023 03:24:44 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from bcd.services.visual.config import VisualConfig
from bcd.services.io.file import IOService

sns.set_style(VisualConfig.style)
sns.set_palette = sns.dark_palette(VisualConfig.palette.blue, reverse=True, as_cmap=True)


# ------------------------------------------------------------------------------------------------ #
#                                    CANCERMETA                                                    #
# ------------------------------------------------------------------------------------------------ #
class CancerMeta(ABC):
    """Base class for CBIS-DDSM metadata.

    Args:
        filepath (str): Path to the metadata file.
        name (str): Name for the Dataset
        train (bool): Wether the dataset is the training dataset. False if it is the test set.
        io (type[IOService]): IOService class for handling file io.
    """

    def __init__(
        self,
        train_filepath: str,
        test_filepath: str,
        name: str,
        io: IOService = IOService,
    ) -> None:
        self._train_filepath = train_filepath
        self._test_filepath = test_filepath
        self._name = name
        self._io = io
        self._train = self._io.read(filepath=train_filepath)
        self._test = self._io.read(filepath=test_filepath)

    @property
    def cases(self) -> int:
        """Returns the number of cases in the dataset."""
        d = {
            "Training Cases": self._train["patient_id"].nunique(),
            "Test Cases": self._test["patient_id"].nunique(),
        }
        return d

    @property
    def abnormalities(self) -> int:
        """Returns the number of abnormalities in the dataset."""
        d = {
            "Training Abnormalities": self._train.shape[0],
            "Test Abnormalities": self._test.shape[0],
        }
        return d

    def pathology(self) -> None:
        """Plots the pathology by number of cases."""

        canvas = VisualConfig().canvas
        ax = canvas.ax
        fig = canvas.fig
        suptitle = f"{self._name}\nPathology"
        fig.suptitle(suptitle)

        d1 = {"Pathology": self._train["pathology"]}
        df1 = pd.DataFrame(data=d1)
        df1["Dataset"] = "Train"

        d2 = {"Pathology": self._test["pathology"]}
        df2 = pd.DataFrame(data=d2)
        df2["Dataset"] = "Test"
        df = pd.concat([df1, df2], axis=0)

        _ = sns.countplot(
            data=df, x="Pathology", hue="Dataset", ax=ax, palette=VisualConfig.palette.blues_r
        )
        for container in ax.containers:
            ax.bar_label(container)

    def assessment(self, ax: plt.axes = None) -> None:
        """Plots the BIRADS assesment by number of cases."""
        canvas = VisualConfig().canvas
        ax = canvas.ax
        fig = canvas.fig
        suptitle = f"{self._name}\nAssessment"
        fig.suptitle(suptitle)

        d1 = {"Assessment": self._train["assessment"]}
        df1 = pd.DataFrame(data=d1)
        df1["Dataset"] = "Train"

        d2 = {"Assessment": self._test["assessment"]}
        df2 = pd.DataFrame(data=d2)
        df2["Dataset"] = "Test"
        df = pd.concat([df1, df2], axis=0)

        _ = sns.countplot(
            data=df, x="Assessment", hue="Dataset", ax=ax, palette=VisualConfig.palette.blues_r
        )
        for container in ax.containers:
            ax.bar_label(container)

    def subtlety(self) -> None:
        """Plots the subtlety by number of cases."""
        canvas = VisualConfig().canvas
        ax = canvas.ax
        fig = canvas.fig
        suptitle = f"{self._name}\nSubtlety"
        fig.suptitle(suptitle)

        d1 = {"Subtlety": self._train["subtlety"]}
        df1 = pd.DataFrame(data=d1)
        df1["Dataset"] = "Train"

        d2 = {"Subtlety": self._test["subtlety"]}
        df2 = pd.DataFrame(data=d2)
        df2["Dataset"] = "Test"
        df = pd.concat([df1, df2], axis=0)

        _ = sns.countplot(
            data=df, x="Subtlety", hue="Dataset", ax=ax, palette=VisualConfig.palette.blues_r
        )
        for container in ax.containers:
            ax.bar_label(container)

    def density(self) -> None:
        """Plots the breast density by number of cases."""
        canvas = VisualConfig().canvas
        ax = canvas.ax
        fig = canvas.fig
        suptitle = f"{self._name}\nBreast Density"
        fig.suptitle(suptitle)

        d1 = {"Breast Density": self._train["breast_density"]}
        df1 = pd.DataFrame(data=d1)
        df1["Dataset"] = "Train"

        d2 = {"Breast Density": self._test["breast_density"]}
        df2 = pd.DataFrame(data=d2)
        df2["Dataset"] = "Test"
        df = pd.concat([df1, df2], axis=0)

        _ = sns.countplot(
            data=df, x="Breast Density", hue="Dataset", ax=ax, palette=VisualConfig.palette.blues_r
        )
        for container in ax.containers:
            ax.bar_label(container)

    def pathology_density(self) -> None:
        """Plots the pathology by density."""
        canvas = VisualConfig(nrows=2, ncols=1).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nPathology by Breast Density"
        fig.suptitle(suptitle)

        ax1 = sns.countplot(
            x=self._train["breast_density"],
            hue=self._train["pathology"],
            ax=ax1,
            palette=VisualConfig.palette.blues_r,
        )
        ax1.get_legend().remove()
        title = "Train Set"
        ax1.set_title(title)

        ax2 = sns.countplot(
            x=self._test["breast_density"],
            hue=self._test["pathology"],
            ax=ax2,
            palette=VisualConfig.palette.blues_r,
        )
        ax2.get_legend().remove()
        title = "Test Set"
        ax2.set_title(title)

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=9)
        plt.tight_layout()

    def pathology_assessment(self) -> None:
        """Plots the pathology by assessment."""
        canvas = VisualConfig(nrows=2, ncols=1, figsize=(6, 3)).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nPathology by BIRADS Assessment"
        fig.suptitle(suptitle)

        ax1 = sns.countplot(
            x=self._train["assessment"],
            hue=self._train["pathology"],
            ax=ax1,
            palette=VisualConfig.palette.blues_r,
        )
        ax1.get_legend().remove()
        title = "Train Set"
        ax1.set_title(title)

        ax2 = sns.countplot(
            x=self._test["assessment"],
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

    def overview(self) -> None:
        """Overview of the Dataset"""
        df = pd.concat([self._train, self._test], axis=0)
        # Benign
        benign_cases = df[df["pathology"] != "MALIGNANT"]["patient_id"].nunique()
        benign_abs = (
            df[df["pathology"] != "MALIGNANT"][["patient_id", "abnormality id"]]
            .drop_duplicates()
            .shape[0]
        )
        mal_cases = df[df["pathology"] == "MALIGNANT"]["patient_id"].nunique()
        mal_abs = (
            df[df["pathology"] == "MALIGNANT"][["patient_id", "abnormality id"]]
            .drop_duplicates()
            .shape[0]
        )

        d = {
            "Pathology": ["Benign", "Benign", "Malignant", "Malignant"],
            "Aggregate": ["Cases", "Abnormalities", "Cases", "Abnormalities"],
            "Count": [benign_cases, benign_abs, mal_cases, mal_abs],
        }
        df = pd.DataFrame.from_dict(data=d, orient="columns")

        canvas = VisualConfig(nrows=1, ncols=1, figsize=(12, 3)).canvas
        ax = canvas.axs
        ax = sns.barplot(
            data=df,
            x="Pathology",
            y="Count",
            hue="Aggregate",
            ax=ax,
            palette=VisualConfig.palette.blues_r,
        )

    def summary(self) -> None:
        """Summarizes the number of cases and abnormalities benign and malignant."""
        canvas = VisualConfig(nrows=1, ncols=2, figsize=(6, 4)).canvas
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        suptitle = f"{self._name}\nCases and Abnormalities"
        fig.suptitle(suptitle)

        # Benign Data
        train = self._train[self._train["pathology"] != "MALIGNANT"]
        test = self._test[self._test["pathology"] != "MALIGNANT"]
        df1 = self._extract_data(train=train, test=test)
        ax1 = sns.barplot(
            data=df1,
            x="Dataset",
            y="Count",
            hue="Aggregate",
            palette=VisualConfig.palette.blues_r,
            ax=ax1,
        )
        ax1.legend_.set_title(None)
        ax1.set_title("Benign")
        for container in ax1.containers:
            ax1.bar_label(container)
        ax1.set(xlabel=None)

        # Malignant Train
        train = self._train[self._train["pathology"] == "MALIGNANT"]
        test = self._test[self._test["pathology"] == "MALIGNANT"]
        df2 = self._extract_data(train=train, test=test)
        ax2 = sns.barplot(
            data=df2,
            x="Dataset",
            y="Count",
            hue="Aggregate",
            palette=VisualConfig.palette.blues_r,
            ax=ax2,
        )
        ax2.legend_.set_title(None)
        ax2.set_title("Malignant")
        for container in ax2.containers:
            ax2.bar_label(container)
        ax2.set(xlabel=None)
        plt.tight_layout()

    def _extract_data(self, train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
        """Returns DataFrame with Case and Abnormality Counts"""
        train_cases = train["patient_id"].nunique()
        test_cases = test["patient_id"].nunique()

        train_abs = train[["patient_id", "abnormality id"]].drop_duplicates().shape[0]
        test_abs = test[["patient_id", "abnormality id"]].drop_duplicates().shape[0]
        d = {
            "Dataset": ["Train", "Train", "Test", "Test"],
            "Aggregate": ["Cases", "Abnormalities", "Cases", "Abnormalities"],
            "Count": [train_cases, train_abs, test_cases, test_abs],
        }
        df = pd.DataFrame.from_dict(data=d, orient="columns")
        return df
