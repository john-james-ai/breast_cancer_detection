#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /tests/test_data/test_study/test_image.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 3rd 2023 01:49:56 am                                                  #
# Modified   : Saturday June 3rd 2023 06:45:47 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import inspect
from datetime import datetime
import pytest
import logging
from pprint import pprint

import pydicom

from bcd.data.study.image import DICOMImage, DICOMPassport

LOCATION = "tests/data"
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.image
class TestImage:  # pragma: no cover
    # ============================================================================================ #
    def test_passport_creation(self, registrations, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        for registration in registrations:
            passport = DICOMPassport.create(registration)
            assert (
                passport.uid == passport.series_uid + "_" + os.path.splitext(passport.filename)[0]
            )
            passport.series_uid == registration["series_uid"]
            passport.collection == registration["collection"]
            passport.data_description_uri == registration["data_description_uri"]
            passport.subject_id == registration["subject_id"]
            passport.study_uid == registration["study_uid"]
            passport.study_date == registration["study_date"]
            passport.series_description == registration["series_description"]
            passport.modality == registration["modality"]
            passport.sop_class_name == registration["sop_class_name"]
            passport.sop_class_uid == registration["sop_class_uid"]
            passport.number_of_images == registration["number_of_images"]
            passport.file_size == registration["file_size"]
            passport.file_location == registration["file_location"]
            passport.filename == registration["filename"]
            passport.download_timestamp == registration["download_timestamp"]
            passport.casetype == registration["casetype"]
            passport.fileset == registration["fileset"]

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_passport_asdict(self, registrations, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        passport = DICOMPassport.create(registrations[0])
        d = passport.as_dict()
        assert isinstance(d, dict)
        pprint(d)
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_image_creation(self, registrations, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        passport = DICOMPassport.create(registrations[3])
        filepath = os.path.join(LOCATION, passport.file_location, passport.filename)
        dataset = pydicom.dcmread(filepath)
        image = DICOMImage(passport=passport, dataset=dataset)
        assert isinstance(image.passport, DICOMPassport)
        assert isinstance(image.dataset, pydicom.Dataset)
        pprint(image.passport)

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_str(self, registrations, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        passport = DICOMPassport.create(registrations[4])
        filepath = os.path.join(LOCATION, passport.file_location, passport.filename)
        dataset = pydicom.dcmread(filepath)
        image = DICOMImage(passport=passport, dataset=dataset)
        assert isinstance(image.passport, DICOMPassport)
        assert isinstance(image.dataset, pydicom.Dataset)
        logger.debug(image.passport)
        assert isinstance(image.uid, str)

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)
