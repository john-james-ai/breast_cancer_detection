#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Breast Cancer Detection from Mammography using Deep Learning                        #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /bcd/services/visual/config.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/breast_cancer_detection                            #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 24th 2023 04:11:27 pm                                                 #
# Modified   : Thursday May 25th 2023 01:19:28 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------------------------ #
#                                            PALETTE                                               #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Palette:
    blue: str = "#69d"
    blues: str = "Blues"
    blues_r: str = "Blues_r"
    dark_blue: str = "dark:b"
    dark_blue_reversed: str = "dark:b_r"
    heatmap: str = "mako"
    bluegreen: str = "crest"
    link: str = "https://colorhunt.co/palette/002b5b2b4865256d858fe3cf"


# ------------------------------------------------------------------------------------------------ #
#                                            CANVAS                                                #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Canvas:
    figsize: tuple
    nrows: int = 1
    ncols: int = 1
    fig: plt.figure = None
    ax: plt.axes = None
    axs: List = field(default_factory=lambda: [plt.axes])

    def __post_init__(self) -> None:
        if self.nrows > 1 or self.ncols > 1:
            figsize = []
            figsize.append(self.figsize[0] * self.ncols)
            figsize.append(self.figsize[1] * self.nrows)
            self.fig, self.axs = plt.subplots(nrows=self.nrows, ncols=self.ncols, figsize=figsize)
        else:
            self.fig, self.ax = plt.subplots(
                nrows=self.nrows, ncols=self.ncols, figsize=self.figsize
            )


# ------------------------------------------------------------------------------------------------ #
#                                            CONFIG                                                #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class VisualConfig:
    style = "whitegrid"
    nrows: int = 1
    ncols: int = 1
    figsize: tuple = (12, 3)
    palette: Palette = Palette()
    canvas: type[Canvas] = None

    def __post_init__(self) -> None:
        self.canvas = Canvas(figsize=self.figsize, nrows=self.nrows, ncols=self.ncols)
