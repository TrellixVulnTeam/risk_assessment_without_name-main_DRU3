"""Supplier Scoring Module"""
from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def company_picker(company_list):
    company_name = st.sidebar.selectbox("Please pick the company name", company_list)
    return company_name

def basic_information(dataframe, company_name):
    with st.expander("Basic Information"):
        st.markdown(f"__Organisation Name__: {company_name}")
        st.markdown(f"__Address__: {list(dataframe['address'][dataframe['company name'].str.contains(company_name)])[0]}")

def metrics_count(dataframe, company_name):
    dataframe = dataframe[dataframe["company name"].str.contains(company_name)]
    st.write(dataframe)
    nc_counts, gfsi_doc_counts, audit_grade, audit_status = st.columns(4)
    with nc_counts:
        st.metric("Number of Nonconformities changes", list(dataframe["total_ncs"])[0], " - 1 NCs", delta_color="inverse")

    with gfsi_doc_counts:
        st.metric("Number of GFSI Docs have on system", 1, "Remain the same", delta_color= "off")

    with audit_grade:
        st.metric("Audit Report Grade", list(dataframe["audit grade"])[-1], "Remain the same", delta_color= "off")

    with audit_status:
        st.metric("Audit Report Status", "Valid")

def instruction():
    with st.expander("INSTRUCTION"):
        st.markdown("For best user experience and easier to visualize, please use __MALT PRODUCT INTERNATIONAL COMPANY__")

def ncs_graph(dataframe, company_name):
    filtered_data = dataframe[dataframe["company name"].str.contains(company_name)].sort_values(by="certificate expiry date")
    nc_line = go.Figure()
    nc_line.add_trace(go.Scatter(x=filtered_data["certificate expiry date"], y=filtered_data["minor"], mode="lines+markers", name="Minor Nonconformities"))
    nc_line.add_trace(go.Scatter(x=filtered_data["certificate expiry date"], y=filtered_data["major"], mode="lines+markers", name="Major Nonconformities"))
    nc_line.add_trace(go.Scatter(x=filtered_data["certificate expiry date"], y=filtered_data["critical"], mode="lines+markers", name="Critical Nonconformities"))
    nc_line.update_layout(
                   xaxis_title='Date Expiry',
                   yaxis_title='Number of Nonconformities',
                   margin=dict(l=10, r=400, t=10, b=50), width=1500,height=400)
    nc_line.update_xaxes(showgrid=False, zeroline=False)
    st.plotly_chart(nc_line)

def scoring():
    instruction()
    data = pd.read_csv("data/brc_otrafyprod.csv").drop_duplicates()
    company_name = company_picker(list(set((data["company name"]))))
    basic_information(data, company_name)
    metrics_count(data, company_name)
    ncs_graph(data, company_name)