#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /cadx/data/entity/meta.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 10:50:00 pm                                                  #
# Modified   : Thursday May 25th 2023 11:29:20 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Metadata Entities"""
from __future__ import annotations

import pandas as pd
from dataclasses import dataclass, field
from data.entity.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Case(Entity):
    density: str
    breast: str
    view: str
    number: int
    type: int
    assessment: int
    pathology: str
    subtlety: int
    image_filepath: str
    roi_filepath: str
    cropped_filepath: str


# ------------------------------------------------------------------------------------------------ #
@dataclass
class MassCase(Case):
    density: str
    breast: str
    view: str
    number: int
    type: int
    mass_shape: str
    mass_margin: str
    assessment: int
    pathology: str
    subtlety: int
    image_filepath: str
    roi_filepath: str
    cropped_filepath: str

    @classmethod
    def factory(cls, case: pd.DataFrame) -> MassCase:
        return cls(
            density=case["density"],
            breast=case["breast"],
            view=case["view"],
            number=case["number"],
            type=case["type"],
            mass_shape=case["mass_shape"],
            mass_margin=case["mass_margin"],
            assessment=case["assessment"],
            pathology=case["pathology"],
            subtlety=case["subtlety"],
            image_filepath=case["image_filepath"],
            roi_filepath=case["roi_filepath"],
            cropped_filepath=case["cropped_filepath"],
        )


# ------------------------------------------------------------------------------------------------ #
@dataclass
class CalcCase(Case):
    density: str
    breast: str
    view: str
    number: int
    type: int
    calc_type: str
    calc_dist: str
    assessment: int
    pathology: str
    subtlety: int
    image_filepath: str
    roi_filepath: str
    cropped_filepath: str

    @classmethod
    def factory(cls, case: pd.DataFrame) -> MassCase:
        return cls(
            density=case["density"],
            breast=case["breast"],
            view=case["view"],
            number=case["number"],
            type=case["type"],
            calc_type=case["calc_type"],
            calc_dist=case["calc_distribution"],
            assessment=case["assessment"],
            pathology=case["pathology"],
            subtlety=case["subtlety"],
            image_filepath=case["image_filepath"],
            roi_filepath=case["roi_filepath"],
            cropped_filepath=case["cropped_filepath"],
        )


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Patient(Entity):
    cases: list[Entity] = field(default_factory=list)

    def get_case(self, abnormality_id: int) -> Case:
        """Returns a case for the patient.

        Args:
            abnormality_id (int): The number of the abnormality
        """
        for case in self.cases:
            if case.id == abnormality_id:
                return case

    @classmethod
    def factory(cls, patient: pd.DataFrame) -> MassCase:
        if "mass" in patient.columns:
            case_template = CalcCase
        else:
            case_template = MassCase

        cases = []
        for idx, row in patient.iterrows():
            case = case_template.factory(row)
            cases.append(case)
        return cls(id=patient["id"][0], cases=cases)
