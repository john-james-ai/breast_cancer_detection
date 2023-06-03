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
# Modified   : Friday June 2nd 2023 08:42:57 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DICOM Repository"""
import os
import pathlib
import logging
import pandas as pd
import pydicom

from bcd.data.repo.base import Repo
from bcd.service.io.file import IOService
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
        self._registry.add(registration=series.as_dict())
        self._save_registry(series)

                self._register_dataset(dataset=dataset)
                self._write(dataset=dataset, filepath=filepath)

    def get(self, study_uid: str) -> pydicom.Dataset:
        """Reads a DICOM dataset and returns a pydicom.FileDataset instance

        Args:
            study_uid (str): The study uid for the dataset.
        """
        metadata = self._get_metadata(study_uid=study_uid)
        self._logger.debug(f"Metadata:\n{metadata}")
        return self._read(metadata["file_location"])

    def get_random(
        self, casetype: str = None, test: bool = False, random_state: int = None
    ) -> pydicom.Dataset:
        """Returnss a randomly selected dataset.

        Args:
            casetype (str): Either 'mass', or 'calc' or None.
            test (bool): If True, return a series from the test set; otherwise, return a series from the training set.
        """
        fileset = "test" if test is True else "train"
        self._load_registry()

        if casetype is None:
            study_uid = (
                self._registry.loc[self._registry["fileset"] == fileset]
                .sample(n=1, random_state=random_state)["study_uid"]
                .values[0]
            )
            self._logger.debug(f"Study uid: {study_uid}")
            return self.get(study_uid=study_uid)
        else:
            study_uid = (
                self._registry.loc[
                    (self._registry["fileset"] == fileset)
                    & (self._registry["casetype"] == casetype)
                ]
                .sample(n=1, random_state=random_state)["study_uid"]
                .values[0]
            )
            self._logger.debug(f"Study uid: {study_uid}")
            return self.get(study_uid=study_uid)

    def update(self, dataset: pydicom.Dataset, filepath: str) -> None:
        """Updates a DICOM file in the repository.

        The file must exist (obviously) and the repository cannot be immutable.

        Args:
            dataset (pydicom.Dataset): A pydicom Dataset instance.
            filepath (str): A filepath within the repository.
        """
        if pathlib.PurePath(filepath).is_relative_to(self._location):
            if os.path.exists(filepath):
                with open(filepath, "wb") as outfile:
                    dataset.save_as(outfile)

    def delete(self, filepath) -> None:
        """Deletes a DICOM file

        Args:
            filepath (str): Path to the file to be deleted.

        """
        if self._immutable:
            msg = "The repository read-only. File can not be deleted."
            self._logger.error(msg)
            raise PermissionError(msg)

        if pathlib.PurePath(filepath).is_relative_to(self._location):
            try:
                os.remove(filepath)
            except FileNotFoundError as e:
                msg = f"Unable to delete file. File {filepath} not found."
                self._logger.error(msg)
                raise e

        else:
            msg = f"Cannot delete files in {filepath} which are outside of the repository base directory {self._location}."
            self._logger.error(msg)
            raise PermissionError(msg)

    def _read(self, filepath) -> pydicom.Dataset:
        """Reads a pydicom Dataset from the repository."""
        if pathlib.PurePath(filepath).is_relative_to(self._location):
            filepath = self._construct_filepath(filepath)
            self._logger.debug(f"Read Filepath: {filepath}")
            try:
                with open(filepath, "rb") as infile:
                    return pydicom.dcmread(infile)
            except Exception as e:
                msg = (
                    f"Unable to read the DICOM dataset.\nException of type {type(e)} occurred.\n{e}"
                )
                self._logger.error(msg)
                raise e
        else:
            msg = f"Unable to read files outside of the repository base directory: {self._location}."
            self._logger.error(msg)
            raise PermissionError(msg)

    def _write(self, dataset: pydicom.Dataset, filepath: str) -> None:
        """Saves a pydicom Dataset to the repository."""
        if pathlib.PurePath(filepath).is_relative_to(self._location):
            try:
                with open(filepath, "wb") as outfile:
                    dataset.save_as(outfile)
            except Exception as e:
                msg = f"Unable to save file. Exception of type {type(e)} occurred.\n{e}"
                self._logger.error(msg)
                raise e

        else:
            msg = f"Cannot save files to {filepath}. Files must be relative to the repository base directory {self._location}."
            self._logger.error(msg)
            raise PermissionError(msg)

    def _get_metadata(self, study_uid: str) -> dict:
        """Returns the filepath for a study id from the registry"""
        metadata = self._registry.loc[self._registry["study_uid"] == study_uid]
        if len(metadata) == 0:
            msg = f"Study UID {study_uid} is invalid."
            self._logger.error(msg)
            raise FileNotFoundError(msg)
        return metadata.to_dict(orient="records")[0]



    def _add_to_registry(self, series: Series) -> None:
        """Adds a series to the registry"""
        self._load_registry()
        if not self._series_exists(series=series):
            self._registry = pd.concat([self._registry, series.as_df()], axis=0)
        else:
            msg = f"Series {series.series_uid} already exists."
            self._logger.error(msg)
            raise FileExistsError(msg)
        self._save_registry()

    def _update_registry(self, series: Series) -> None:
        """Adds a series to the registry"""
        self._load_registry()
        if self._series_exists(series=series):
            self._remove_from_registry(series_uid=series.series_uid)
            self._add_to_registry(series=series)
        else:
            msg = f"Series {series.series_uid} does not exist."
            self._logger.error(msg)
            raise FileNotFoundError(msg)
        self._save_registry()


    def _remove_from_registry(self, series_uid) -> None:
        """Removes a series from the registry"""
        self._load_registry()
        self._registry = self._registry.loc[self._registry['series_uid'] == series_uid]
        self._save_registry()

    def _validate_series(self, series: Series, exist_ok: bool = False) -> None:
        """Validates series object.

        Args:
            series (Series): The Series object
        """
        msg = ""
        if self._immutable:
            msg += "The operation is invalid on an immutable series."
        elif not exist_ok and self._series_exists(series):
            msg += f"Series {series.series_uid} already exists."
        elif not pathlib.PurePath(series.file_location).is_relative_to(self._location):
            msg += f"Series location {series.file_location} is not relative to repository base directory {self._location}."
        elif len(series.datasets) == 0:
            msg += "The datasets member is empty."
        elif len(series.datasets) != series.number_of_images:
            msg += f"The length of the datasets member, {len(series.datasets)} does not match 'number_of_images' = {series.number_of_images}.\n"
        elif series.casetype not in ['mass', 'calc']:
            msg += f"Series case type, {series.casetype} is invalid. Valid values are 'mass', and 'calc'."
        elif series.fileset not in ['train', 'test']:
            msg += f"Series file set, {series.fileset} is invalid. Valid values are 'train', and 'test'."

        if len(msg) > 0:
            self._logger.error(msg)
            raise Exception(msg)
