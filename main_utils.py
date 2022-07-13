"""Main.py Utility Module"""
from __future__ import annotations
from typing import List, Dict

import pandas as pd
import streamlit as st

from source.single_file_analysis.sa_analysis import analysis as sa_analysis
from source.cross_analysis.cross_analysis import analysis as cross_analysis
from source.supplier_scoring import scoring

def select_function():
    add_selectbox = st.sidebar.selectbox(
        "How do you want to analysis the files ?",
        ("Cross-Analysis", "Single File Analysis", "Supplier Scoring")
    )
    if add_selectbox == "Cross-Analysis":
        cross_analysis()
    elif add_selectbox == "Single File Analysis":
        sa_analysis()
    elif add_selectbox == "Supplier Scoring":
        scoring()

    return add_selectbox