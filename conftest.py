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
# Modified   : Wednesday May 31st 2023 04:52:54 am                                                 #
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
DATAFILE = "tests/data/meta/test_data1.csv"

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
    # Reset the environment variable to test.
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ["MODE"] = "test"
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])

    container = BCDContainer()
    container.init_resources()
    # container.wire(packages=[])

    return container
