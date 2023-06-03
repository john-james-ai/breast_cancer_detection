#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/repo/registry.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday June 2nd 2023 06:46:16 pm                                                    #
# Modified   : Saturday June 3rd 2023 01:34:37 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #


import pandas as pd

from bcd.data.repo.base import Registry


# ------------------------------------------------------------------------------------------------ #
class SeriesRegistry(Registry):
    """Registry for DICOM series

    Args:
        filepath (str): Location of registry

    """

    def __init__(self, filepath: str, immutable: bool) -> None:
        super().__init__(filepath=filepath, immutable=immutable)

    @property
    def count(self) -> int:
        """Returns number of registered series'."""
        return len(self.get_uids())

    def add(self, registration: dict) -> None:
        """Adds a series registration to the registry."""
        self._load()

        if not self._exists(series_uid=registration["series_uid"]):
            registration = pd.DataFrame(data=registration, index=[0])
            self._registry = pd.concat([self._registry, registration], axis=0)
        else:
            msg = f"Series uid {registration['series_uid']} already exists."
            self._logger.error(msg)
            raise FileExistsError(msg)
        self._save()

    def get(self, series_uid: str) -> dict:
        """Gets a registration for a series from the registry.

        Args:
            series _uid (str): Series unique id.
        """
        self._load()
        if self._exists(series_uid):
            return self._registry[self._registry["series_uid"] == series_uid].to_dict(
                orient="records"
            )[0]
        else:
            msg = f"The series_uid, {series_uid} does not exist."
            self._logger.error(msg)
            raise FileNotFoundError(msg)

    def get_uids(self) -> list:
        """Returns a list of series uids"""
        self._load()
        return self._registry["series_uid"].values

    def update(self, registration: dict) -> None:
        """Updates the registration in the registry

        Args:
            registration (dict): Series registration
        """

        self.remove(series_uid=registration["series_uid"])
        self.add(registration=registration)

    def remove(self, series_uid: str) -> None:
        """Removes a Series registration from the registry."""
        self._load()
        if self._exists(series_uid=series_uid):
            self._registry = self._registry[self._registry["series_uid"] != series_uid]
        else:
            msg = f"Series registration for {series_uid} not found."
            self._logger.error(msg)
            raise FileNotFoundError(msg)
        self._save()

    def _exists(self, series_uid: str) -> bool:
        """Checks existence of the series in the registry."""
        self._load()
        try:
            return series_uid in self._registry["series_uid"].values
        except KeyError:
            return False
