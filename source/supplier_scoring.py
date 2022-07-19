"""Supplier Scoring Module"""
from __future__ import annotations

import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from source.utility import check_date
from source.api.fda_dashboard import inspections_citations_api, inspections_classification_api, import_refusals_api
from source.api.fdc_api import call_api as fdc_api

def company_picker(company_list):
    company_name = st.sidebar.selectbox(
        "Please pick the company name", company_list)
    return company_name


def basic_information(dataframe, company_name):
    with st.expander("Basic Information"):
        st.markdown(f"__Organisation Name__: {company_name}")
        try:
            st.markdown(
                f"__Address__: {list(dataframe['address'][dataframe['company name'].str.contains(company_name)])[0]}")
        except KeyError:
            st.markdown(
                f"__Address__: {list(dataframe['company name'][dataframe['company name'].str.contains(company_name)])[0]}")


def metrics_count(dataframe, company_name):
    dataframe = dataframe[dataframe["company name"].str.contains(company_name)].sort_values(by = "certificate expiry date", ascending = False)
    ncs_list = list(dataframe["total_ncs"][dataframe["company name"].str.contains(company_name)])
    st.write(dataframe)
    try:
        score_changes = ncs_list[0] - ncs_list[1]
    except IndexError:
        score_changes = ncs_list[0]

    nc_counts, audit_grade, audit_status = st.columns(3)
    with nc_counts:
        if ncs_list[0] == score_changes:
            st.metric("Number of Nonconformities changes", ncs_list[0], "0 NCs", delta_color="off")
        else:
            st.metric("Number of Nonconformities changes", ncs_list[0], f" {score_changes} NCs", delta_color="inverse")

    with audit_grade:
        st.metric("Audit Report Grade", list(
            dataframe["audit grade"])[-1], delta_color="off")

    with audit_status:
        exp_date = list(dataframe["certificate expiry date"])[0]
        if check_date(datetime.datetime.strptime(exp_date, "%m/%d/%Y").date()):
            st.metric("Audit Report Status", "Valid")
        else:
            st.metric("Audit Report Status", "Expired")


def instruction():
    with st.expander("INSTRUCTION"):
        st.markdown(
            "For best user experience and easier to visualize, please use __MALT PRODUCT INTERNATIONAL COMPANY__")


def ncs_graph(dataframe, company_name):
    filtered_data = dataframe[dataframe["company name"].str.contains(
        company_name)].sort_values(by="certificate expiry date")
    nc_line = go.Figure()
    nc_line.add_trace(go.Scatter(x=filtered_data["certificate expiry date"],
                      y=filtered_data["minor"], mode="lines+markers", name="Minor Nonconformities"))
    nc_line.add_trace(go.Scatter(x=filtered_data["certificate expiry date"],
                      y=filtered_data["major"], mode="lines+markers", name="Major Nonconformities"))
    nc_line.add_trace(go.Scatter(x=filtered_data["certificate expiry date"],
                      y=filtered_data["critical"], mode="lines+markers", name="Critical Nonconformities"))
    nc_line.update_layout(
        xaxis_title='Date Expiry',
        yaxis_title='Number of Nonconformities',
        margin=dict(l=10, r=400, t=10, b=50), width=1500, height=400)
    nc_line.update_xaxes(showgrid=False, zeroline=False)
    nc_line.update_yaxes(showgrid=False, zeroline=False)
    st.plotly_chart(nc_line)

def connect_to_fda_dashboard(dataframe, company_name):
    dataframe = dataframe[dataframe["company name"].str.contains(company_name)].sort_values(by = "certificate expiry date", ascending = False)
    with st.expander("INSPECTIONS CITATIONS FDA"):
        st.write(inspections_citations_api(list(dataframe["cleaned company name"])))
    
    with st.expander("INSPECTIONS CLASSIFICATIONS FDA"):
        st.write(inspections_classification_api(list(dataframe["cleaned company name"])))
    
    with st.expander("IMPORT REFUSAL FDA"):
        st.write(import_refusals_api(list(dataframe["cleaned company name"])))

def connect_to_fdc_dashboard(dataframe, company_name):
    dataframe = dataframe[dataframe["company name"].str.contains(company_name)].sort_values(by = "certificate expiry date", ascending = False)
    with st.expander("RELATED PRODUCT"):
        try:
            st.write(fdc_api(list(dataframe["cleaned company name"])[0]))
        except KeyError:
            st.write("No Information")


def scoring():
    instruction()
    data = pd.read_csv("data/whole_df.csv").drop_duplicates(subset=["certificate expiry date"])
    company_name = company_picker(list(set((data["company name"]))))
    basic_information(data, company_name)
    metrics_count(data, company_name)
    ncs_graph(data, company_name)
    connect_to_fda_dashboard(data, company_name)
    connect_to_fdc_dashboard(data, company_name)
