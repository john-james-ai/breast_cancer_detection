#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/study/series.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday June 2nd 2023 02:48:55 pm                                                    #
# Modified   : Friday June 2nd 2023 09:27:03 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Series Module"""
from __future__ import annotations
import os
from datetime import datetime

import logging
from dataclasses import dataclass, field

import pandas as pd
import pydicom

from bcd import IMMUTABLE_TYPES, SEQUENCE_TYPES


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Series:
    """Encapsulates a study series of DICOM images and all behaviors thereto."""

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
    number_of_images: int
    file_size: float
    file_location: str
    download_timestamp: str
    casetype: str
    fileset: str
    filenames = list[str] = field(default_factor=list)
    datasets = list[pydicom.Dataset] = field(default=list)  # list of in-memory pydicom.Datasets

    def __post_init__(self) -> None:
        self.images = os.listdir(self.file_location)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @classmethod
    def create(cls, metadata: dict) -> Series:
        return cls(
            series_uid=metadata["series_uid"],
            collection=metadata["collection"],
            data_description_uri=metadata["data_description_uri"],
            subject_id=metadata["subject_id"],
            study_uid=metadata["study_uid"],
            study_date=metadata["study_date"],
            series_description=metadata["series_description"],
            modality=metadata["modality"],
            sop_class_name=metadata["sop_class_name"],
            sop_class_uid=metadata["sop_class_uid"],
            number_of_images=metadata["number_of_images"],
            file_size=metadata["file_size"],
            file_location=metadata["file_location"],
            download_timestamp=metadata["download_timestamp"],
            casetype=metadata["casetype"],
            fileset=metadata["fileset"],
        )

    def load(self) -> None:
        """Loads the DICOM files into the list of Datasets."""
        filepaths = [
            os.path.join(self.file_location, filename)
            for filename in os.listdir(self.file_location)
        ]
        for i, filepath in enumerate(filepaths):
            try:
                self.datasets[i] = pydicom.dcmread(filepath)
            except Exception as e:
                msg = f"Exception of type {type(e)} occurred.\n{e}"
                self._logger.error(msg)
                raise e

    def save(self) -> None:
        """Saves the pydicom Datasets to files in DICOM format, if mutable."""
        if self.immutable:
            msg = "Series is immutable. Write to another location or change the immutability of this series."
            self._logger.error(msg)
            raise PermissionError(msg)
        else:
            filepaths = [
                os.path.join(self.file_location, filename)
                for filename in os.listdir(self.file_location)
            ]

            for i, filepath in enumerate(filepaths):
                try:
                    pydicom.dcmwrite(filename=filepath, dataset=self.datasets[i])
                except Exception as e:
                    msg = f"Exception of type {type(e)} occurred.\n{e}"
                    self._logger.error(msg)
                    raise e

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Legend object."""
        return {k: self._export_field(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_field(cls, v):  # pragma: no cover
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

    def as_df(self) -> pd.DataFrame:
        """Returns series as a pandas DataFrame"""
        d = self.as_dict()
        return pd.DataFrame(data=d, index=[0])
