#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /bcd/data/repo/meta.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 10:56:21 pm                                                  #
# Modified   : Wednesday May 31st 2023 04:39:03 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from datetime import datetime
import logging
from typing import Any

import pandas as pd

from bcd.data.repo.base import Repo
from bcd.services.io.file import IOService


# ------------------------------------------------------------------------------------------------ #
class MetaRepo(Repo):
    def __init__(self, directory: str, io: IOService) -> None:
        self._directory = directory
        self._registry = None
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def registry(self) -> pd.DataFrame:
        self._load_registry()
        return self._registry

    def get(self, filename: str) -> Any:
        """Reads a file from the repository."""
        filepath = os.path.join(self._directory, filename)
        try:
            return self._io.read(filepath=filepath)
        except Exception as e:
            msg = f"File {filename} does not exist."
            self._logger.error(msg)
            raise FileNotFoundError(e)

    def add(self, filename: str, data: Any, force: bool = False) -> None:
        """Adds a file to the repository"""
        filepath = os.path.join(self._directory, filename)

        if self.exists(filename) and not force:
            msg = f"File with name {filename} already exists."
            self._logger.error(msg)
            raise FileExistsError(msg)
        elif self.exists(filename):
            msg = "File exists. Forcing will overwrite the file. Are you sure? *y/n "
            overwrite = input(msg)
            if "y" in overwrite.lower():
                self._io.write(filepath, data=data)
        else:
            self._io.write(filepath, data=data)

    def exists(self, filename) -> bool:
        """Checks existence of a file"""
        filepath = os.path.join(self._directory, filename)
        return os.path.exists(filepath)

    def _load_registry(self):
        filedata = []
        filenames = os.listdir(self._directory)
        for filename in filenames:
            filepath = os.path.join(self._directory, filename)
            d = {
                "Filename": filename,
                "Size": os.path.getsize(filepath),
                "Created": datetime.fromtimestamp(os.path.getctime(filepath)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Modified": datetime.fromtimestamp(os.path.getmtime(filepath)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
            filedata.append(d)
        self._registry = pd.DataFrame(data=filedata)
