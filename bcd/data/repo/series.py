#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/repo/series.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 1st 2023 10:15:55 pm                                                  #
# Modified   : Friday June 2nd 2023 09:43:40 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DICOM Repository"""
import os
import pandas as pd
import pydicom
import shutil

from bcd.data.repo.base import Repo
from bcd.data.study.series import Series
from bcd.data.repo.registry import SeriesRegistry


# ------------------------------------------------------------------------------------------------ #
class SeriesRepo(Repo):
    """Encapsulates the IO for DICOM series'

    Args:
        location (str): Base directory for the repository
        registry (Registry)
        io (IOService): File reader/writer

    """

    def __init__(
        self,
        location: str,
        registry: SeriesRegistry,
        immutable: bool = True,
    ) -> None:
        super().__init__(location=location, registry=registry, immutable=immutable)

    @property
    def registry(self) -> pd.DataFrame:
        """Returns the registry in DataFrame format."""
        return self._registry.registry

    def add(self, series: Series) -> None:
        """Adds a DICOM series to the repository.

        Args:
            series (Series): A pydicom Dataset or subclass thereof.

        """
        self._check_mutability()
        self._registry.add(registration=series.as_dict())
        self._save_registry(series)

    def get(self, series_uid: str) -> Series:
        """Obtain a Series from the repository

        Args:
            series_uid (str): Unique identifier for the series
        """
        registration = self._registry.get(series_uid=series_uid)
        series = Series.create(metadata=registration)
        return self._load(series=series)

    def update(self, series: Series) -> None:
        """Update an existing Series

        Args:
            series (Series): A pydicom Dataset or subclass thereof.
        """
        self._check_mutability()
        self._registry.update(registration=series.as_dict())
        self._save(series=series)

    def remove(self, series_uid: str) -> None:
        """Removes a series from the repository"""
        self._check_mutability()
        registration = self._registry.get(series_uid=series_uid)
        self._registry.remove(series_uid=series_uid)
        self._delete(location=registration["file_location"])

    def _load(self, series: Series) -> Series:
        """Loads the series images from file."""

        datasets = []

        directory = os.path.join(self._location, series.file_location)
        for filename in series.filenames:
            filepath = os.path.join(directory, filename)
            try:
                dataset = pydicom.dcmread(fp=filepath)
                datasets.append(dataset)
            except Exception as e:
                msg = f"Exception of type {type(e)} occurred.\n{e}"
                self._logger.error(msg)
                raise e

        series.datasets = datasets
        return series

    def _save(self, series: Series) -> None:
        """Saves the series Datasets to file."""
        self._check_mutability()

        directory = os.path.join(self._location, series.file_location)
        os.makedirs(directory, exist_ok=True)

        for filename, dataset in zip(series.filenames, series.datasets):
            filepath = os.path.join(directory, filename)
            try:
                pydicom.dcmwrite(filename=filepath, dataset=dataset)
            except Exception as e:
                msg = f"Exception of type {type(e)} occurred.\n{e}"
                self._logger.error(msg)
                raise e

    def _delete(self, location: str) -> None:
        """Deletes a series from disk"""
        shutil.rmtree(location)
