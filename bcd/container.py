#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Deep Learning Methods for Breast Cancer Detection                                   #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/container.py                                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 12:43:06 pm                                                  #
# Modified   : Wednesday May 31st 2023 02:50:02 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import os
import logging
import logging.config  # pragma: no cover
from dotenv import load_dotenv

from dependency_injector import containers, providers

from bcd.data.repo.meta import MetaRepo
from bcd.services.io.file import IOService


# ------------------------------------------------------------------------------------------------ #
#                                    CONFIG SELECTOR                                               #
# ------------------------------------------------------------------------------------------------ #
class DataDirSelector:
    __datadirs = {"test": "tests/data/", "dev": "data/dev/", "prod": "data/prod/"}

    def __call__(self) -> str:
        """Returns the config file based upon mode, i.e 'test', or 'prod'"""
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

        load_dotenv()
        mode = os.getenv("MODE")
        datadir = self.__datadirs[mode]
        os.environ.setdefault("DATADIR", datadir)


# ------------------------------------------------------------------------------------------------ #
#                                        LOGGING                                                   #
# ------------------------------------------------------------------------------------------------ #
class LoggingContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


# ------------------------------------------------------------------------------------------------ #
#                                         REPOS                                                    #
# ------------------------------------------------------------------------------------------------ #
class RepoContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    meta = providers.Singleton(MetaRepo, directory=config.repos.meta, io=IOService)


# ------------------------------------------------------------------------------------------------ #
#                                       FRAMEWORK                                                  #
# ------------------------------------------------------------------------------------------------ #
class BCDContainer(containers.DeclarativeContainer):
    select = DataDirSelector()

    select()

    config = providers.Configuration(yaml_files=["config.yml"])

    logging.info(config)

    logs = providers.Container(LoggingContainer, config=config)

    repo = providers.Container(RepoContainer, config=config)