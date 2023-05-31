#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /deepcad/data/repo/base.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 10:26:59 pm                                                  #
# Modified   : Wednesday May 31st 2023 12:21:58 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Base Repo class"""

    @property
    @abstractmethod
    def registry(self) -> pd.DataFrame:
        """Returns the file registry"""

    @abstractmethod
    def get(self, filename: str) -> Any:
        """Gets a file from the repository."""

    @abstractmethod
    def add(self, filename: str, data: Any) -> None:
        """Adds a file to the repository."""

    @abstractmethod
    def exists(filename: str) -> bool:
        """Determines whether file by the name already exists."""
