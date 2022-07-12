"""Main function"""
from __future__ import annotations
from urllib.request import urlopen

import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from source.main_utils import select_function, upload_file, classify_file_type
from source.information_extraction.brc_ocr import brc_scan
from source.information_extraction.sqf_ocr import sqf_scan

def main() -> None:
    """Main function to run the app"""
    st.title("Third Party Audit Analysis")
    function_name = select_function()
    file_list = upload_file()
    file_type_dict = {file_list[0].name : "BRC Audit"}
    #file_type_dict = classify_file_type(file_list)

    for file_value in file_list:
        result_extract = {}
        filename = file_value.name
        if file_type_dict[filename] == "BRC Audit":
            result_dict = brc_scan(file_value, result_extract)



main()
