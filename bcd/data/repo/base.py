#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /bcd/data/repo/base.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 10:26:59 pm                                                  #
# Modified   : Saturday June 3rd 2023 05:06:32 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Repository Base Module"""
from __future__ import annotations
import os
from abc import ABC, abstractmethod
import logging
from typing import Any

import pandas as pd

from bcd.service.io.file import IOService


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Base Repo class"""

    def __init__(self, location: str, registry: Registry, immutable: bool) -> None:
        self._location = location
        self._registry = registry
        self._immutable = immutable
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def immutable(self) -> bool:
        """Returns the value of the immutability variable."""
        return self._immutable

    @immutable.setter
    def immutable(self, immutable: bool) -> None:
        """Sets the immutability of the Repo"""
        self._immutable = immutable

    @property
    @abstractmethod
    def registry(self) -> pd.DataFrame:
        """Returns the registry for the repository"""

    @abstractmethod
    def get(self, *args, **kwargs) -> Any:
        """Gets an entity from the repository."""

    @abstractmethod
    def add(self, *args, **kwargs) -> Any:
        """Adds an entity to the repository."""

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        """Updates an existing entity in the repository."""

    @abstractmethod
    def remove(self, *args, **kwargs) -> Any:
        """Removes an existing entity from the repository."""

    def _check_mutability(self) -> None:
        """Raises exception if instance is immutable"""
        if self._immutable:
            msg = f"{self.__class__.__name__} instance is immutable."
            self._logger.error(msg)
            raise PermissionError(msg)


# ------------------------------------------------------------------------------------------------ #
class Registry(ABC):
    def __init__(self, filepath: str, io: IOService = IOService) -> None:
        self._filepath = filepath
        self._io = io
        self._registry = pd.DataFrame()
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def registry(self) -> pd.DataFrame:
        """Returns the registry."""
        return self._registry

    @abstractmethod
    def get(self, *args, **kwargs) -> pd.DataFrame:
        """Get an item from the registry."""

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        """Adds an item to the registry."""

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Updates an existing registration in the registry."""

    @abstractmethod
    def remove(self, *args, **kwargs) -> None:
        """Removes an item from the registry."""

    def _load(self, force: bool = False) -> None:
        """Loads the registry into the instance variable."""
        try:
            self._registry = self._io.read(self._filepath, index_col=None)
        except FileNotFoundError:
            self._registry = pd.DataFrame()
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.error(msg)
            raise e

    def _save(self) -> None:
        """Saves the instance variable to file."""
        try:
            os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
            self._io.write(data=self._registry, filepath=self._filepath)
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            self._logger.error(msg)
            raise e
