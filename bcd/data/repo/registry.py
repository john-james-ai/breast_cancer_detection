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
# Modified   : Saturday June 3rd 2023 05:09:36 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #


import pandas as pd

from bcd.data.repo.base import Registry


# ------------------------------------------------------------------------------------------------ #
class ImageRegistry(Registry):
    """Registry for DICOM image

    Args:
        filepath (str): Location of registry

    """

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath=filepath)

    @property
    def count(self) -> int:
        """Returns number of registered images'."""
        return len(self.get_uids())

    def add(self, registration: dict) -> None:
        """Adds a image registration to the registry."""
        self._load()

        if not self._exists(uid=registration["uid"]):
            # Convert the registration to DataFrame format and append to registry
            registration = pd.DataFrame(data=registration, index=[0])
            self._registry = pd.concat([self._registry, registration], axis=0)
        else:
            msg = f"Image uid {registration['uid']} already exists."
            self._logger.error(msg)
            raise FileExistsError(msg)
        self._save()

    def get(self, uid: str) -> dict:
        """Gets a registration for a image from the registry.

        Args:
            image _uid (str): Image unique id.
        """
        self._load()
        if self._exists(uid):
            return self._registry[self._registry["uid"] == uid].to_dict(orient="records")[
                0
            ]  # Actually returns a list
        else:
            msg = f"The uid, {uid} does not exist."
            self._logger.error(msg)
            raise FileNotFoundError(msg)

    def get_uids(self) -> list:
        """Returns a list of image uids"""
        self._load()
        return self._registry["uid"].values

    def update(self, registration: dict) -> None:
        """Updates the registration in the registry

        Args:
            registration (dict): Image registration
        """

        self.remove(uid=registration["uid"])
        self.add(registration=registration)

    def remove(self, uid: str) -> None:
        """Removes a Image registration from the registry."""
        self._load()
        if self._exists(uid=uid):
            self._registry = self._registry[self._registry["uid"] != uid]
        else:
            msg = f"Image registration for {uid} not found."
            self._logger.error(msg)
            raise FileNotFoundError(msg)
        self._save()

    def _exists(self, uid: str) -> bool:
        """Checks existence of the image in the registry."""
        self._load()
        try:
            return uid in self._registry["uid"].values
        except KeyError:
            return False
