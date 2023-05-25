---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# Data

## CBIS-DDSM Dataset

The Curated Breast Imaging Subset (CBIS) of the Digital Database for Screening Mammography (DDSM) dataset, otherwise known as the CBIS-DDSM dataset {cite}`leeCuratedMammographyData2017a`, includes decompressed images, data selected and curated by trained mammographers, mass segmentation, bounding boxes, and pathological diagnoses, in Digital Imaging and Communications in Medicine (DICOM) format.

```python
import matplotlib.pyplot as plt

from bcd.services.visual.config import VisualConfig
from bcd.data.explore.metadata import MassMeta, CalcMeta

```
