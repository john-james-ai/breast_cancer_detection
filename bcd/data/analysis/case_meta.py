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
# Modified   : Friday June 2nd 2023 02:56:55 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dependency_injector.wiring import Provide, inject
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from bcd.data.repo.meta import CaseMetaRepo
from bcd.service.visual.config import Canvas
from bcd.container import BCDContainer

sns.set_style(Canvas.style)
sns.set_palette = sns.dark_palette(Canvas.color, reverse=True, as_cmap=True)
# ------------------------------------------------------------------------------------------------ #


class CaseMeta:
    """Encapsulates the calcification and mass metadata."""

    __calc_cases = "calc_cases.csv"
    __mass_cases = "mass_cases.csv"

    @inject
    def __init__(self, repo: CaseMetaRepo = Provide[BCDContainer.repo.meta]) -> None:
        self._repo = repo
        self._calc = self._repo.get(casetype="calc")
        self._mass = self._repo.get(casetype="mass")

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

    def pathology_feature(self, top: int = 5) -> None:
        """Plots top n features by pathology and abnormality type"""
        canvas = Canvas(nrows=2, ncols=2, figsize=(6, 3))
        fig = canvas.fig
        ((ax1, ax2), (ax3, ax4)) = canvas.axs
        title = f"Top {top} Features by Pathology"
        fig.suptitle(title)

        self._pathology_feature(data=self._calc, feature="calc_type", ax=ax1, top=top)
        self._pathology_feature(data=self._calc, feature="calc_distribution", ax=ax2, top=top)
        self._pathology_feature(data=self._mass, feature="mass_shape", ax=ax3, top=top)
        self._pathology_feature(data=self._mass, feature="mass_margins", ax=ax4, top=top)

    def _pathology_feature(
        self, data: pd.DataFrame, feature: str, ax: plt.axes, top: int = 5
    ) -> None:
        """Plots top n features by pathology"""
        labels = {
            "calc_type": "Calcification Type",
            "calc_distribution": "Calcification Distribution",
            "mass_shape": "Mass Shape",
            "mass_margins": "Mass Margins",
        }
        label = labels[feature]

        df = (
            data.groupby(by=["pathology", feature])
            .size()
            .reset_index(name="count")
            .sort_values(by=["pathology", "count"], ascending=False)
        )
        df = df.groupby(by="pathology").head(top)
        df.columns = ["Pathology", label, "Count"]

        ax = sns.barplot(
            data=df,
            x="Pathology",
            y="Count",
            hue=label,
            ax=ax,
            saturation=0.5,
            estimator="sum",
            dodge=False,
            palette=Canvas.palette,
        )

        ax.set_title(label)
        ax.legend(loc="best", fontsize=6, framealpha=0.3, mode="expand", ncols=2)
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
