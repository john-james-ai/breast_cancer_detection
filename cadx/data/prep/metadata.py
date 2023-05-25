#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.10                                                                             #
# Filename   : /cadx/data/prep/metadata.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday May 25th 2023 07:32:20 am                                                  #
# Modified   : Thursday May 25th 2023 12:38:05 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

import pandas as pd
import numpy as np


# ------------------------------------------------------------------------------------------------ #
class ColumnTransformer:
    """Removes spaces from column names and replaces them with underscores."""

    def fit(self, X: pd.DataFrame, y: np.array = None) -> ColumnTransformer:
        return self

    def transform(self, X: pd.DataFrame, y: np.array = None) -> pd.DataFrame:
        mapping = {col: col.replace(" ", "_") for col in X.columns}
        return X.rename(columns=mapping)
