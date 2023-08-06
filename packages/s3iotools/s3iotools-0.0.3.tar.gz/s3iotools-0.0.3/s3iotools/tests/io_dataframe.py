# -*- coding: utf-8 -*-

import os
import pandas as pd

df_customers = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "customers.tsv"),
    sep="\t",
    encoding="utf8",
)
