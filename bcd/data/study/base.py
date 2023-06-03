#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/study/base.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 3rd 2023 02:41:25 am                                                  #
# Modified   : Saturday June 3rd 2023 04:53:43 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Passport(ABC):
    """Encapsulates all metadata for an image"""


# ------------------------------------------------------------------------------------------------ #
class Image(ABC):
    """Encapsulates a medical image dataset."""

    @property
    @abstractmethod
    def uid(self) -> str:
        """Exposes the uid for the dataset."""

    @property
    @abstractmethod
    def dataset(self) -> Any:
        """Returns the dataset"""
