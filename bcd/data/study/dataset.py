#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/data/study/dataset.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 3rd 2023 02:35:07 am                                                  #
# Modified   : Saturday June 3rd 2023 03:09:27 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging

import pydicom

from bcd.data.study.base import Dataset

# ------------------------------------------------------------------------------------------------ #


class DICOMDataset(Dataset):
    """Encapsulates a DICOM Dataset

    Args:
        series_uid (str): The unique id for the series to which the dataset belongs
        filename (str): The name of the file, without the the filepath.
    """

    def __init__(self, study_uid: str, filename: str) -> None:
        self._uid = study_uid + "_" + filename
        self._study_uid = study_uid
        self._filename = filename
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def dataset(self) -> pydicom.Dataset:
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: pydicom.Dataset) -> None:
        self._dataset = dataset
