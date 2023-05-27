#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /cadx/data/repo/base.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 10:26:59 pm                                                  #
# Modified   : Thursday May 25th 2023 10:43:58 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

from data.entity.meta import Case, Patient


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Base Repo class"""

    @property
    @abstractmethod
    def density(self) -> dict:
        """Returns dictionary of density counts."""

    @property
    @abstractmethod
    def assessment(self) -> dict:
        """Returns number of assessments"""

    @property
    @abstractmethod
    def pathology(self) -> dict:
        """Returns pathology counts"""

    @property
    @abstractmethod
    def sublety(self) -> dict:
        """Returns sublety counts"""

    @abstractmethod
    def get_patient(self, patient_id: str) -> Patient:
        """ "Returns a patient object."""

    @abstractmethod
    def get_case(self, patient_id: str, abnormality_number: int) -> Case:
        """Returns  a case."""

    @abstractmethod
    def load(self) -> None:
        """Loads data into the repo."""

    @abstractmethod
    def save(self) -> None:
        """Saves repo to file"""
