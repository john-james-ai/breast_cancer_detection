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
# Modified   : Saturday June 3rd 2023 06:35:30 am                                                  #
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

from bcd.data.repo.registry import ImageRegistry
from bcd.container import BCDContainer

# ------------------------------------------------------------------------------------------------ #
DATAFILE = "tests/data/meta/calc_cases.csv"
DICOMDIR = "tests/data/CBIS-DDSM"
METADATA = "tests/data/meta/metadata.csv"
REGISTRY = "tests/data/CBIS-DDSM/registry.csv"
LOCATION = "tests/data"
# ------------------------------------------------------------------------------------------------ #
collect_ignore_glob = []


# ------------------------------------------------------------------------------------------------ #
#                                       DATASET                                                    #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def dataset():
    return pd.read_csv(DATAFILE)


# ------------------------------------------------------------------------------------------------ #
#                                    REGISTRATIONS                                                 #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def registrations():
    meta = pd.read_csv(METADATA, index_col=None)
    meta = meta[
        (meta["file_location"].str.contains("Calc-Test_P_00140"))
        | (meta["file_location"].str.contains("Mass-Test_P_00145"))
    ]
    registrations = []
    for _, row in meta.iterrows():
        directory = os.path.join(LOCATION, row["file_location"].replace("./", ""))
        filenames = os.listdir(directory)
        for filename in filenames:
            row["filename"] = filename
            row = dict(row)
            registrations.append(row)
    return registrations


# ------------------------------------------------------------------------------------------------ #
#                                      REGISTRY                                                    #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def registry():
    return ImageRegistry(filepath=REGISTRY)


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
