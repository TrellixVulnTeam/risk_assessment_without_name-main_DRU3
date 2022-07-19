"""FDA Data Dashboard Connection Database Module"""
from __future__ import annotations

import requests
import pandas as pd
import streamlit as st

PAYLOAD = {}
HEADERS = {
  'Content-Type': 'application/json',
  'Authorization-User': 'huy@otrafy.com',
  'Authorization-Key': 'XHS3OAH8K2E1FOS'
}

def construct_dataframe(json):
    dataframe = pd.DataFrame(json)
    return dataframe

def call_api(url, body):
    response = requests.request("POST", url, headers= HEADERS, data= PAYLOAD, json = body)
    return construct_dataframe(response.json()["result"])

def inspections_citations_api(legal_name):
    body = {
    "sort": "",
    "sortorder": "",
    "rows" : 100,
    "filters" : {},
    "columns" : []
    }
    URL = 'https://api-datadashboard.fda.gov/v1/inspections_citations?'
    body["filters"] = {"LegalName": legal_name}
    result = call_api(URL,body)
    return result

def import_refusals_api(firm_name):
    body = {
    "sort": "",
    "sortorder": "",
    "rows" : 100,
    "filters" : {},
    "columns" : []
    }
    URL = 'https://api-datadashboard.fda.gov/v1/import_refusals?'
    body["filters"] = {"FirmName": firm_name}
    result = call_api(URL, body)
    return result

def inspections_classification_api(legal_name):
    body = {
    "sort": "",
    "sortorder": "",
    "rows" : 100,
    "filters" : {},
    "columns" : []
    }
    URL = 'https://api-datadashboard.fda.gov/v1/inspections_classifications?'
    body["filters"] = {"LegalName": legal_name}
    result = call_api(URL, body)
    return result

