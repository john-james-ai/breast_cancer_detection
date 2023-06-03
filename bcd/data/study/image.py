#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/study/image.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday June 2nd 2023 02:48:55 pm                                                    #
# Modified   : Saturday June 3rd 2023 06:39:05 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Series Module"""
from __future__ import annotations
import os
from datetime import datetime
from dataclasses import dataclass, fields
import logging

import pydicom

from bcd import IMMUTABLE_TYPES, SEQUENCE_TYPES
from bcd.data.study.base import Image, Passport


# ------------------------------------------------------------------------------------------------ #
@dataclass
class DICOMPassport(Passport):
    """Encapsulates the metadata for a DICOM image"""

    series_uid: str
    collection: str
    data_description_uri: str
    subject_id: str
    study_uid: str
    study_date: str
    series_description: str
    modality: str
    sop_class_name: str
    sop_class_uid: str
    number_of_images: str
    file_size: int
    file_location: str
    filename: str
    download_timestamp: str
    casetype: str
    fileset: str
    uid: str = None

    def __post_init__(self) -> None:
        self.uid = self.series_uid + "_" + os.path.splitext(self.filename)[0]

    def __str__(self) -> str:
        width = 32
        msg = f"\n\n{self.__class__.__name__}\n"
        for k, v in self.__dict__.items():
            msg += f"\t{k.rjust(width, ' ')} | {v}\n"
        return msg

    def __repr__(self) -> str:
        msg = f"{self.__class__.__name__}("
        for k, v in self.__dict__.items():
            msg += f"{k}={v}, "
        msg += ")"
        msg = msg.replace(", )", ")")
        return msg

    @classmethod
    def create(cls, params: dict) -> DICOMPassport:
        """Creates a Passport object from a dictionary"""
        attributes = [f.name for f in fields(cls) if f.init]
        filtered_params = {k: v for k, v in params.items() if k in attributes}
        return cls(**filtered_params)

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Legend object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):  # pragma: no cover
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v
        elif isinstance(v, dict):
            return v
        elif hasattr(v, "as_dict"):
            return v.as_dict()
        else:
            """Else nothing. What do you want?"""


# ------------------------------------------------------------------------------------------------ #
class DICOMImage(Image):
    """Encapsulates a DICOM image and all behaviors thereto."""

    def __init__(self, passport: Passport, dataset: pydicom.Dataset) -> None:
        self._passport = passport
        self._dataset = dataset
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def uid(self) -> str:
        return self._passport.uid

    @property
    def passport(self) -> dict:
        return self._passport

    @property
    def dataset(self) -> list:
        """Returns the DICOM dataset"""
        return self._dataset
