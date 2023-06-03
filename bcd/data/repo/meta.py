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
# Modified   : Friday June 2nd 2023 02:56:55 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
from typing import Any

from bcd.data.repo.base import Repo
from bcd.service.io.file import IOService


# ------------------------------------------------------------------------------------------------ #
class CaseMetaRepo(Repo):
    __filepaths = {
        "calc": "data/dev/meta/calc_cases.csv",
        "mass": "data/dev/meta/mass_cases.csv",
    }

    def __init__(self, io: IOService) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def info(self, casetype: str) -> None:
        """Wraps pandas DataFrame info method.

        Args:
            casetype (str): Either 'calc', or 'mass'.
        """
        try:
            filepath = self.__filepaths[casetype]
        except KeyError as e:
            msg = f"Case type {casetype} is invalid. Must be in ['calc','mass']"
            self._logger.error(msg)
            raise FileNotFoundError(e)
        self._io.read(filepath=filepath).info()

    def get(self, casetype: str) -> Any:
        """Returns metadata for the designated casetype from the repository

        Args:
            casetype (str): Either 'calc', or 'mass'.

        ."""
        try:
            filepath = self.__filepaths[casetype]
        except KeyError as e:
            msg = f"Case type {casetype} is invalid. Must be in ['calc','mass']"
            self._logger.error(msg)
            raise FileNotFoundError(e)
        return self._io.read(filepath=filepath)
