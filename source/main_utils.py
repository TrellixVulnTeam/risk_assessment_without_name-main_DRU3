"""Main.py Utility Module"""
from __future__ import annotations
from typing import List, Dict

import streamlit as st

import source.classification as classification

def upload_file() -> List:
    file_list = st.file_uploader("Start Upload File",
                                 type = ["pdf"],
                                 accept_multiple_files = True)

    return file_list

def classify_file_type(file_list) -> Dict:
    result = {}
    for file_value in file_list:
        filename = file_value.name
        bytes_data = file_value.read()
        doc_type = classification.inference_image(bytes_data)
        result[filename] = doc_type

    return result

def select_function():
    add_selectbox = st.sidebar.selectbox(
        "How do you want to analysis the files ?",
        ("Cross-Analysis", "Single File Analysis", "Supplier Scoring")
    )
    if add_selectbox == "Cross-Analysis":
        pass
    elif add_selectbox == "Single File Analysis":
        pass
    elif add_selectbox == "Supplier Scoring":
        pass

    return add_selectbox