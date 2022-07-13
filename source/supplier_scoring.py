"""Supplier Scoring Module"""
from __future__ import annotations

import pandas as pd
import streamlit as st

def company_picker(company_list):
    company_name = st.sidebar.selectbox("Please pick the format", company_list)
    return company_name

def basic_information(dataframe, company_name):
    with st.expander("Basic Information"):
        st.markdown(f"__Organisation Name__: {company_name}")
        st.markdown(f"__Address__: {list(dataframe['address'][dataframe['company name'].str.contains(company_name)])[0]}")

def scoring():
    data = pd.read_csv("data/brc_otrafyprod.csv").drop_duplicates()
    company_name = company_picker(list(set((data["company name"]))))
    basic_information(data, company_name)