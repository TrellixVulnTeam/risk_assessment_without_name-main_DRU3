"""Single File Analysis Module"""
from __future__ import annotations

import pandas as pd
import streamlit as st


def format_picker():
    format_type = st.sidebar.selectbox(
        "Please pick the format", ["BRC", "SQF"])
    return format_type


def company_picker(company_list):
    company_name = st.sidebar.selectbox("Please pick the format", company_list)
    return company_name


def year_picker(dataframe, company_name):
    year = st.sidebar.selectbox("Please select the expiry year", list(
        dataframe["certificate expiry date"][dataframe["company name"].str.contains(company_name)]))
    return year


def basic_information(dataframe, company_name):
    with st.expander("Basic Information"):
        st.markdown(f"__File name__: {dataframe['filename'][dataframe['company name'].str.contains(company_name)]}")
        st.markdown(f"__Organisation Name__: {company_name}")
        try:
            st.markdown(
                f"__Address__: {list(dataframe['address'][dataframe['company name'].str.contains(company_name)])[0]}")
        except KeyError:
            st.markdown(
                f"__Address__: {list(dataframe['company name'][dataframe['company name'].str.contains(company_name)])[0]}")


def nc_counts(dataframe, company_name, year):
    total_nc = dataframe["minor"][dataframe["company name"].str.contains(company_name) & dataframe["certificate expiry date"].str.contains(year)].unique(
    )[0] + dataframe["major"][dataframe["company name"].str.contains(company_name)].unique()[0] + dataframe["critical"][dataframe["company name"].str.contains(company_name)].unique()[0]
    with st.expander("Nonconformities Breakdown"):
        st.markdown(f'__Total Nonconformities__: {total_nc}')
        st.markdown(
            f'__Minor Nonconformities__: {dataframe["minor"][dataframe["company name"].str.contains(company_name) & dataframe["certificate expiry date"].str.contains(year)].unique()[0]}')
        st.markdown(
            f'__Major Nonconformities__: {dataframe["major"][dataframe["company name"].str.contains(company_name)].unique()[0]}')
        st.markdown(
            f'__Critical Nonconformities__: {dataframe["critical"][dataframe["company name"].str.contains(company_name)].unique()[0]}')


def audit_result(dataframe, company_name, year):
    with st.expander("Audit Outcome"):
        st.markdown(
            f"__Audit Grade__: {list(dataframe['audit grade'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")
        st.markdown(
            f"__Audit Result__: {list(dataframe['audit result'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")
        st.markdown(
            f"__Audit Type__: {list(dataframe['audit type'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")

    with st.expander("Previous Audit Information"):
        try:
            st.markdown(
                f"__Previous Audit Grade__: {list(dataframe['previous audit grade'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")
            st.markdown(
                f"__Previous Audit Date__: {list(dataframe['previous audit date'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")
        except KeyError:
            st.markdown("Unavailable")

    with st.expander("3PA Certificate Information"):
        st.markdown(
            f"__Certificate Issue Date__: {list(dataframe['certificate issue date'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")
        st.markdown(
            f"__Certificate Expiry Date__: {list(dataframe['certificate expiry date'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")


def auditor_info(dataframe, company_name, year):
    with st.expander("Auditor Related Information"):
        st.markdown(
            f"__Auditor Company__: {list(dataframe['auditor company'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")
        st.markdown(
            f"__Auditor Name__: {list(dataframe['auditor name'][dataframe['company name'].str.contains(company_name) & dataframe['certificate expiry date'].str.contains(year)])[0]}")


def analysis():
    format_type = format_picker()
    data = pd.read_csv(f"data/{format_type.lower()}_otrafyprod.csv").drop_duplicates(subset=["company name"])
    company_name = company_picker(list(set((data["company name"]))))
    year = year_picker(data, company_name)
    basic_information(data, company_name)
    nc_counts(data, company_name, year)
    audit_result(data, company_name, year)
    auditor_info(data, company_name, year)
