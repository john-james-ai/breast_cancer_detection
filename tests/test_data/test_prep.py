#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /tests/test_data/test_prep.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 07:41:39 am                                                  #
# Modified   : Wednesday May 31st 2023 12:21:59 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging
import pandas as pd

from bcd.data.prep.metadata import ColumnTransformer


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #
CALC_TRAIN_FILEPATH = "data/ext/calc_case_description_train_set.csv"
CALC_TEST_FILEPATH = "data/ext/calc_case_description_test_set.csv"
MASS_TRAIN_FILEPATH = "data/ext/mass_case_description_train_set.csv"
MASS_TEST_FILEPATH = "data/ext/mass_case_description_test_set.csv"


@pytest.mark.colx4mr
class TestColX4mr:  # pragma: no cover
    # ============================================================================================ #
    def test_setup(self, caplog):
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
        df = pd.read_csv(CALC_TRAIN_FILEPATH)
        x4mr = ColumnTransformer()
        df2 = x4mr.fit(df).transform(X=df)
        cols = df2.columns
        for col in cols:
            assert " " not in col
            logger.debug(col)

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
