#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /cadx/data/repo/meta.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 10:56:21 pm                                                  #
# Modified   : Friday May 26th 2023 03:14:39 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd

from data.repo.base import Repo
from services.io.file import IOService
from data.entity.meta import Patient, Case


# ------------------------------------------------------------------------------------------------ #
class MetaRepo(Repo):
    __name = "CalcificationRepo"

    def __init__(self, train_filepath: str, test_filepath: str, name: str) -> None:
        self._train_filepath = train_filepath
        self._test_filepath = test_filepath
        self._name = name or self.__name
        self._io = IOService()

        self._density = None
        self._assessment = None
        self._pathology = None
        self._sublety = None

    @property
    def density(self) -> pd.DataFrame:
        """Returns dictionary of density counts."""
        if self._density is None:
            self._density = self._df["breast_density"].value_counts()
        return self._density

    @property
    def assessment(self) -> dict:
        """Returns number of assessments"""
        if self._assessment is None:
            self._assessment = self._df["assessment"].value_counts()
        return self._assessment

    @property
    def pathology(self) -> dict:
        """Returns pathology counts"""
        if self._pathology is None:
            self._pathology = self._df["pathology"].value_counts()
        return self._pathology

    @property
    def sublety(self) -> dict:
        """Returns sublety counts"""
        if self._sublety is None:
            self._sublety = self._df["sublety"].value_counts()
        return self._sublety

    def get_patient(self, patient_id: str) -> Patient:
        """ "Returns a patient object."""
        df = self._df[self._df["patient_id"] == patient_id]
        return Patient.factory(patient=df)

    def get_case(self, patient_id: str, abnormality_number: int) -> Case:
        """Returns  a case."""
        patient = self.get_patient(patient_id=patient_id)
        return patient.get_case(abnormality_id=abnormality_number)

    def load(self) -> None:
        """Loads data into the repo."""
        df1 = self._io.read(filepath=self._train_fileath)
        df2 = self._io.read(filepath=self._test_fileath)
        self._df = pd.concat([df1, df2], axis=0)

    def save(self) -> None:
        """Saves repo to file"""
        raise NotImplementedError
