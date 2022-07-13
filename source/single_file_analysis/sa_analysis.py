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

def nc_counts(brc_dataframe, company_name):
    total_nc = brc_dataframe["minor"][brc_dataframe["company name"].str.contains(company_name)].unique()[0] + brc_dataframe["major"][brc_dataframe["company name"].str.contains(company_name)].unique()[0] + brc_dataframe["critical"][brc_dataframe["company name"].str.contains(company_name)].unique()[0] + brc_dataframe["fundamental"][brc_dataframe["company name"].str.contains(company_name)].unique()[0]
    with st.expander("Nonconformities Breakdown"):
        st.markdown(f'__Total Nonconformities__: {total_nc}')
        st.markdown(f'__Minor Nonconformities__: {brc_dataframe["minor"][brc_dataframe["company name"].str.contains(company_name)].unique()[0]}')
        st.markdown(f'__Major Nonconformities__: {brc_dataframe["major"][brc_dataframe["company name"].str.contains(company_name)].unique()[0]}')
        st.markdown(f'__Critical Nonconformities__: {brc_dataframe["critical"][brc_dataframe["company name"].str.contains(company_name)].unique()[0]}')
        st.markdown(f'__Fundamental Nonconformities__: {brc_dataframe["fundamental"][brc_dataframe["company name"].str.contains(company_name)].unique()[0]}')

def audit_result(brc_dataframe, company_name):
    with st.expander("Audit Outcome"):
        st.markdown(f"__Audit Grade__: {list(brc_dataframe['audit grade'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
        st.markdown(f"__Audit Result__: {list(brc_dataframe['audit result'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
        st.markdown(f"__Audit Type__: {list(brc_dataframe['audit type'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
    
    with st.expander("Previous Audit Information"):
        st.markdown(f"__Previous Audit Grade__: {list(brc_dataframe['previous audit grade'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
        st.markdown(f"__Previous Audit Date__: {list(brc_dataframe['previous audit date'][brc_dataframe['company name'].str.contains(company_name)])[0]}")

    with st.expander("3PA Certificate Information"):
        st.markdown(f"__Certificate Issue Date__: {list(brc_dataframe['certificate issue date'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
        st.markdown(f"__Certificate Expiry Date__: {list(brc_dataframe['certificate expiry date'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
    
def auditor_info(brc_dataframe, company_name):
    with st.expander("Auditor Related Information"):
        st.markdown(f"__Auditor Company__: {list(brc_dataframe['auditor company'][brc_dataframe['company name'].str.contains(company_name)])[0]}")
        st.markdown(f"__Auditor Name__: {list(brc_dataframe['auditor name'][brc_dataframe['company name'].str.contains(company_name)])[0]}")

def analysis():
    format_type = format_picker()
    data = pd.read_csv(f"data/{format_type.lower()}_otrafyprod.csv")
    company_name = company_picker(list(set((data["company name"]))))
    basic_information(data, company_name)
    nc_counts(data, company_name)
    audit_result(data, company_name)
    auditor_info(data, company_name)


