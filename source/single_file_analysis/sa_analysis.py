"""Single File Analysis Module"""
from __future__ import annotations

import pandas as pd
import streamlit as st

def format_picker():
    format_type = st.sidebar.selectbox("Please pick the format", ["BRC", "SQF"])
    return format_type

def company_picker(company_list):
    company_name = st.sidebar.selectbox("Please pick the format", company_list)
    return company_name

def basic_information(brc_dataframe, company_name):
    with st.expander("Basic Information"):
        st.markdown(f"__Organisation Name__: {company_name}")
        st.markdown(f"__Address__: {list(brc_dataframe['address'][brc_dataframe['company name'].str.contains(company_name)])[0]}")

def audit_results(brc_dataframe, company_name):
    with st.expander("Audit Results"):
        

def analysis():
    format_type = format_picker()
    data = pd.read_csv(f"data/{format_type.lower()}_otrafyprod.csv")
    company_name = company_picker(list(data["company name"]))
    basic_information(data, company_name)


