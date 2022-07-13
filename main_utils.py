"""Main.py Utility Module"""
from __future__ import annotations
from typing import List, Dict

import pandas as pd
import streamlit as st

from source.single_file_analysis.sa_analysis import analysis as sa_analysis

def select_function():
    add_selectbox = st.sidebar.selectbox(
        "How do you want to analysis the files ?",
        ("Cross-Analysis", "Single File Analysis", "Supplier Scoring")
    )
    if add_selectbox == "Cross-Analysis":
        pass
    elif add_selectbox == "Single File Analysis":
        sa_analysis()
    elif add_selectbox == "Supplier Scoring":
        pass

    return add_selectbox