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
# Modified   : Wednesday May 31st 2023 02:16:18 am                                                 #
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
#                                  SET MODE TO TEST                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=True)
def mode():
    # Get and save current mode
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    mode = os.environ["MODE"]

    # Change mode to test
    os.environ["MODE"] = "test"
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])
    yield
    # Change mode back to its original value
    os.environ["MODE"] = mode
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])


# ------------------------------------------------------------------------------------------------ #
#                                 DEPENDENCY INJECTION                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=True)
def container():
    container = BCDContainer()
    container.init_resources()
    # container.wire(packages=[])

    return container
