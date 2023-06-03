#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /conftest.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday May 30th 2023 11:25:42 pm                                                   #
# Modified   : Thursday June 1st 2023 10:34:43 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import pytest
import pandas as pd
import dotenv

from bcd.container import BCDContainer

# ------------------------------------------------------------------------------------------------ #
DATAFILE = "tests/data/meta/calc_cases.csv"

# ------------------------------------------------------------------------------------------------ #
collect_ignore_glob = []


# ------------------------------------------------------------------------------------------------ #
#                                       DATASET                                                    #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def dataset():
    return pd.read_csv(DATAFILE)


# ------------------------------------------------------------------------------------------------ #
#                                 DEPENDENCY INJECTION                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=True)
def container():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    # Get current mode
    mode = os.environ["MODE"]

    # Reset the environment variable to test.
    os.environ["MODE"] = "test"
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])

    container = BCDContainer()
    container.init_resources()
    # container.wire(packages=[])

    yield container  # Return mode to prior setting
    os.environ["MODE"] = mode
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])
