#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/analysis/case_meta.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 31st 2023 03:58:20 am                                                 #
# Modified   : Wednesday May 31st 2023 06:07:02 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dependency_injector.wiring import Provide, inject
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from bcd.data.repo.meta import MetaRepo
from bcd.services.visual.config import Canvas
from bcd.container import BCDContainer

sns.set_style(Canvas.style)
sns.set_palette = sns.dark_palette(Canvas.color, reverse=True, as_cmap=True)
# ------------------------------------------------------------------------------------------------ #


class CaseMeta:
    """Encapsulates the calcification and mass metadata."""

    __calc_cases = "calc_cases.csv"
    __mass_cases = "mass_cases.csv"

    @inject
    def __init__(self, repo: MetaRepo = Provide[BCDContainer.repo.meta]) -> None:
        self._repo = repo
        self._calc = self._repo.get(filename=self.__calc_cases)
        self._mass = self._repo.get(filename=self.__mass_cases)

    def cases_and_abnormalities(self) -> None:
        """Renders a plot of counts by pathology and case type"""
        canvas = Canvas(nrows=1, ncols=2, figsize=(6, 4))
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        fig.suptitle("Cases and Abnormalities by Pathology")

        calc_cases = self._case_counts(self._calc)
        mass_cases = self._case_counts(self._mass)

        ax1 = sns.barplot(
            data=calc_cases, x="type", y="count", hue="pathology", ax=ax1, palette=Canvas.palette
        )
        ax2 = sns.barplot(
            data=mass_cases, x="type", y="count", hue="pathology", ax=ax2, palette=Canvas.palette
        )

        for container in ax1.containers:
            ax1.bar_label(container)
        for container in ax2.containers:
            ax2.bar_label(container)

        ax1.set_title("Calcification Cases")
        ax2.set_title("Mass Cases")

        ax1.get_legend().remove()
        ax2.get_legend().remove()

        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=8)

        plt.tight_layout()

    def abnormalities(self, title: str, measure: str, group: str, group_order: list = []) -> None:
        """Renders a plot of counts by pathology and case type

        Args:
            measure (str): The primary feature measure which will be plotted along the x-axis
            group (str): The categorical grouping
        """
        canvas = Canvas(nrows=1, ncols=2, figsize=(6, 4))
        fig = canvas.fig
        (ax1, ax2) = canvas.axs
        fig.suptitle(title)

        ax1 = sns.countplot(
            data=self._calc,
            x=measure,
            hue=group,
            ax=ax1,
            palette=Canvas.palette,
            hue_order=group_order,
        )
        ax2 = sns.countplot(
            data=self._mass,
            x=measure,
            hue=group,
            ax=ax2,
            palette=Canvas.palette,
            hue_order=group_order,
        )

        for container in ax1.containers:
            ax1.bar_label(container)
        for container in ax2.containers:
            ax2.bar_label(container)

        ax1.set_title("Calcification Cases")
        ax2.set_title("Mass Cases")

        ax1.get_legend().remove()
        ax2.get_legend().remove()

        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", fontsize=8)

        plt.tight_layout()

    def _case_counts(self, meta: pd.DataFrame) -> pd.DataFrame:
        """Computes case and abnormality counts by pathology"""
        cases = (
            meta.groupby(by="pathology")["patient_id"]
            .nunique()
            .to_frame()
            .reset_index(names=["pathology", "count"])
        )
        cases["type"] = "cases"
        cases.columns = ["pathology", "count", "type"]
        abnorms = (
            meta.groupby(by="pathology").size().to_frame().reset_index(names=["pathology", "count"])
        )
        abnorms["type"] = "abnormalities"
        abnorms.columns = ["pathology", "count", "type"]
        cases = pd.concat([cases, abnorms], axis=0)
        return cases
