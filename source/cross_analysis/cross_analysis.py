"""Cross Analysis Module"""
from __future__ import annotations

import pandas as pd
import streamlit as st

import plotly.graph_objects as go
import plotly.express as px

def format_picker():
    format_type = st.sidebar.selectbox(
        "Please pick the format", ["BRC", "SQF"])
    return format_type


def data_summarize(dataframe):
    st.markdown("### Audit Report Nonconformities Summarize")

    minor, major, critical = st.columns(3)
    with minor:
        st.metric("Minor Nonconformities", sum(dataframe["minor"]))
        dataframe = dataframe.sort_values("minor", ascending=False)
        top_minor = dataframe[["company name", "minor"]].head().to_dict("list")
        st.write(
            f"__{top_minor['company name'][0]}__: {top_minor['minor'][0]}")
        st.markdown(
            f"__{top_minor['company name'][1]}__: {top_minor['minor'][1]}")
    with major:
        st.metric("Major Nonconformities", sum(dataframe["major"]))
        dataframe = dataframe.sort_values("major", ascending=False)
        top_minor = dataframe[["company name", "major"]].head().to_dict("list")
        st.write(
            f"__{top_minor['company name'][0]}__: {top_minor['major'][0]}")
        st.markdown(
            f"__{top_minor['company name'][1]}__: {top_minor['major'][1]}")
    with critical:
        st.metric("Critical Nonconformities", sum(dataframe["critical"]))
        if sum(dataframe["critical"]) != 0:
            dataframe = dataframe.sort_values("critical", ascending=False)
            top_minor = dataframe[["company name",
                                   "critical"]].head().to_dict("list")
            st.write(
                f"__{top_minor['company name'][0]}__: {top_minor['critical'][0]}")
            st.markdown(
                f"__{top_minor['company name'][1]}__: {top_minor['critical'][1]}")


def audit_grade_summary(dataframe):
    audit_grade_label = dataframe["audit grade"].value_counts().to_dict()
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    audit_grade_graph = go.Figure(data=[go.Pie(labels=list(audit_grade_label.keys(
    )), values=list(audit_grade_label.values()), textinfo='label+value')])
    audit_grade_graph.update_traces(
        hoverinfo='label+percent', textinfo='label+value', showlegend=False)
    audit_grade_graph.update_layout(margin=dict(
        l=10, r=400, t=10, b=50), width=800, height=500)
    st.plotly_chart(audit_grade_graph)


def audit_result_summary(dataframe):
    audit_grade_label = dataframe["audit result"].value_counts().to_dict()
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    audit_result_graph = go.Figure(data=[go.Pie(labels=list(audit_grade_label.keys(
    )), values=list(audit_grade_label.values()), textinfo='label+value')])
    audit_result_graph.update_traces(
        hoverinfo='label+percent', textinfo='label+value', showlegend=False)
    audit_result_graph.update_layout(margin=dict(
        l=10, r=400, t=10, b=50), width=800, height=500)
    st.plotly_chart(audit_result_graph)


def top_best_supplier(dataframe):
    dataframe.sort_values(["minor", "major", "critical"], ascending=[
                          True, True, True], inplace=True)
    try:
        st.table(dataframe[["company name", "address",
                "audit grade", "certificate expiry date"]].head())
    except KeyError:
        st.table(dataframe[["company name",
                "audit grade", "certificate expiry date"]].head())


def top_worst_supplier(dataframe):
    dataframe.sort_values(["minor", "major", "critical"], ascending=[
                          False, False, False], inplace=True)
    try:
        st.table(dataframe[["company name", "address",
                "audit grade", "certificate expiry date"]].head())
    except KeyError:
        st.table(dataframe[["company name",
                "audit grade", "certificate expiry date"]].head())


def score_fluctuate(dataframe):
    score_change = 0
    score_stay = 0
    score_increase = 0
    score_decrease = 0
    score_ranking = ["aa+", "aa", "a", "b+", "b"]
    current_score_list = list(dataframe["audit grade"])
    previous_score_list = list(dataframe["previous audit grade"])

    for current_score, previous_score in zip(current_score_list, previous_score_list):
        try:
            if current_score == previous_score:
                score_stay += 1
            else:
                score_change += 1
                if score_ranking.index(current_score) < score_ranking.index(previous_score):
                    score_increase += 1
                else:
                    score_decrease += 1
        except ValueError:
            pass

    score_fluctuate_column, score_increase_column = st.columns(2)
    with score_fluctuate_column:
        score_fluctuate_graph = go.Figure(data=[go.Pie(labels=["Score remained the same", "Score changed"], values=[
                                          score_stay, score_change], textinfo='label+value')])
        score_fluctuate_graph.update_traces(
            hoverinfo='label+percent', textinfo='label+value', showlegend=False)
        score_fluctuate_graph.update_layout(margin=dict(
            l=10, r=400, t=10, b=50), width=800, height=500)
        st.plotly_chart(score_fluctuate_graph)

    with score_increase_column:
        score_fluctuate_graph = go.Figure(data=[go.Pie(labels=["Score Increased", "Score Decreased"], values=[
                                          score_increase, score_decrease], textinfo='label+value')])
        score_fluctuate_graph.update_traces(
            hoverinfo='label+percent', textinfo='label+value', showlegend=False)
        score_fluctuate_graph.update_layout(margin=dict(
            l=10, r=400, t=10, b=50), width=800, height=500)
        st.plotly_chart(score_fluctuate_graph)


def analysis():
    format_type = format_picker()
    dataframe = pd.read_csv(f"data/{format_type.lower()}_otrafyprod.csv").drop_duplicates(subset=["company name"])
    with st.expander("Dataset Summarise"):
        st.write(dataframe)

    data_summarize(dataframe)

    audit_result, audit_grade = st.columns(2)
    with audit_grade:
        st.markdown("### Audit Grade")
        audit_grade_summary(dataframe)
    with audit_result:
        st.markdown("### Audit Result")
        audit_result_summary(dataframe)

    st.markdown("### Top 5 best supplier")
    top_best_supplier(dataframe)

    st.markdown("### Top 5 worst supplier")
    top_worst_supplier(dataframe)

    if format_type == "BRC":
        st.markdown("### Audit Grade Distribution")
        score_fluctuate(dataframe)
