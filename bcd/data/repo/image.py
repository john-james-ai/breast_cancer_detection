#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/repo/image.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 1st 2023 10:15:55 pm                                                  #
# Modified   : Saturday June 3rd 2023 05:04:46 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""DICOMImage Repository"""
import os
import pandas as pd
import pydicom

from bcd.data.repo.base import Repo
from bcd.data.study.image import DICOMImage, DICOMPassport
from bcd.data.repo.registry import DICOMImageRegistry


# ------------------------------------------------------------------------------------------------ #
class DICOMImageRepo(Repo):
    """Encapsulates access to DICOM DICOMImages stored on disc

    Args:
        location (str): Base directory for the repository
        registry (Registry): Registry for images containing the metadata (passport).
        immutable (bool): Indicates the mutability of the repository

    """

    def __init__(
        self,
        location: str,
        registry: DICOMImageRegistry,
        immutable: bool = True,
    ) -> None:
        super().__init__(location=location, registry=registry, immutable=immutable)

    @property
    def registry(self) -> pd.DataFrame:
        """Returns the registry in DataFrame format."""
        return self._registry.registry

    def add(self, image: DICOMImage) -> None:
        """Adds a DICOM image to the repository.

        Args:
            imae (DICOMImage): A pydicom Dataset or subclass thereof.

        """
        self._check_mutability()
        # Send the passport as dictionary to the registry
        self._registry.add(registration=image.passport.as_dict())
        # Format the filepath combining the repository location and file location in the passport.
        filepath = self._get_filepath(image.passport.as_dict())
        # Save the dataset object to file.
        self._save(dataset=image.dataset, filepath=filepath)

    def get(self, uid: str) -> DICOMImage:
        """Obtain a DICOMImage from the repository

        Args:
            uid (str): Unique identifier for the image
        """
        # Obtain the registration containing the passport attributes of the image from the registry
        registration = self._registry.get(uid=uid)
        # Extract and format the filepath including the repository location
        filepath = self._get_filepath(registration=registration)
        # Load the dataset from the filepath
        dataset = self._load(filepath=filepath)
        # Create the passport object for the image from the registration
        passport = DICOMPassport.create(params=registration)
        # Construct the image object with passport and dataset.
        image = DICOMImage(passport=passport, dataset=dataset)
        return image

    def update(self, image: DICOMImage) -> None:
        """Update an existing DICOMImage

        Args:
            image (DICOMImage): A pydicom Dataset or subclass thereof.
        """
        self._check_mutability()
        # Update the registry
        self._registry.update(registration=image.passport.as_dict())
        # Format the filepath from the repository location
        filepath = self._get_filepath(registration=image.passport.as_dict())
        # Save the dataset object to file.
        self._save(dataset=image.dataset, filepath=filepath)

    def remove(self, uid: str) -> None:
        """Removes a image from the repository

        Args:
            uid (str): The unique identifier for the image.
        """
        self._check_mutability()
        # Get the registration for the image
        registration = self._registry.get(uid=uid)
        # Format and extract the filename for the dataset.
        filepath = self._get_filepath(registration=registration)
        # Remove the dataset
        self._delete(filepath)
        # Remove the registration
        self._registry.remove(uid=uid)

    def _load(self, filepath: str) -> pydicom.Dataset:
        """Loads the image images from file."""

        try:
            return pydicom.dcmread(fp=filepath)
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.error(msg)
            raise e

    def _save(self, dataset: pydicom.Dataset, filepath: str) -> None:
        """Saves the image Datasets to file."""
        try:
            pydicom.dcmwrite(filename=filepath, dataset=dataset)
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.error(msg)
            raise e

    def _delete(self, filepath: str) -> None:
        """Deletes a image from disk"""
        try:
            os.remove(filepath)
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.error(msg)
            raise e

    def _get_filepath(self, registration: dict) -> str:
        """Formats the filepath to the image."""

        try:
            return os.path.join(
                self._location, registration["file_location"], registration["filename"]
            )
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.error(msg)
            raise e
