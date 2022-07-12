"""BRC OCR Module"""
from __future__ import annotations
from io import BytesIO

import re
from typing import Dict, List

import pdfplumber as plumber
import streamlit as st

AUDIT_RESULT_HEADERS = ["audit grade", "audit type", "audit result"]
KEY_HEADERS = [
    "critical",
    "number of non-conformities",
    "fundamental",
    "minor",
    "major",
    "audit start date",
    "audit finish date",
    "re-audit date due date",
    "certificate expiry date",
    "certificate expiry",
    "certificate issue date",
    "site code",
    "previous audit date",
    "site name",
]


def regex_checker(text: str,
                  header_list: List[str],
                  result_extract: Dict[str, str]) -> Dict[str, str]:
    """
    Using regex to extract information out based on header list

    Args:
        text (str): the input text that extract from the pdf file
        HEADER (list): a list of key values that want to extract info from the pdf
        result_extract (Dict[str, str]): the dictionary contains the result

    Returns:
        result_extract (Dict[str, str]): a dictionary that has been updated with newest values
    """
    raw_result = []
    regex_delimiter = re.compile("|".join(header_list))
    splitter = [text.strip()
                for text in regex_delimiter.split(text.lower())[1:]]
    delimiters = regex_delimiter.findall(text.lower())
    if splitter and delimiters:
        groupped = [(splitter, delimiters)]
        raw_result.append(groupped)

    for sub_list in raw_result:
        for key, value in sub_list:
            for index, value in enumerate(value):
                if key[index].strip() != "":
                    result_extract[value[index]] = key[index]

    return result_extract


def get_company_name(pdf_file: BytesIO, result_extract: Dict[str, str]) -> Dict[str, str]:
    """Get the company information

    Args:
        pdf_file (BytesIO): the path to the pdf file
        result_extract (Dict[str, str]): the dictionary that contains the result after extracted

    Returns:
        result_extract (Dict[str, str]): the dictionary that contains the result after extracted has been updated
    """
    with plumber.open(pdf_file) as file:
        doc = file.pages[0]
        word = doc.extract_words()

    non_dup_list = [dict(t) for t in {tuple(d.items()) for d in word}]
    sorted_dictionary = sorted(non_dup_list, key=lambda d: (d["top"], d['x0']))

    range_list = []
    for index, value in enumerate(sorted_dictionary):
        if value["text"] == "Summary":
            range_list.append(index)
        elif value["text"] == "name":
            range_list.append(index)
    result_text_list = [i["text"] for i in sorted_dictionary]

    result_extract["company name"] = " ".join(
        result_text_list[range_list[0] + 1: range_list[1]])
    return result_extract


def extract_date(pdf_file, result_extract: Dict[str, str]) -> Dict[str, str]:
    """Extract the start date audit from the BRC

    Args:
        pdf_file (Path): the path to the pdf file
        result_extract (Dict[str, str]): the dictionary that contains the result after extracted

    Returns:
        result_extract (Dict[str, str]): the dictionary that contains the result after extracted has been updated
    """
    with plumber.open(pdf_file) as file:
        for page in range(2, 5):
            doc = file.pages[page]
            sentence = doc.extract_text(y_tolerance=5).split(
                "\n")  # extract text and split by line
            sentence = [text.strip()
                        for text in sentence if text]  # strip the word
            sentence = [text for text in sentence if text]
            # print(sentence)
            for text in sentence:
                if ("Audit Days" in text) or ("Audit Day" in text):
                    if text:
                        # date returned will be a datetime.datetime object. here we are only using the first match.
                        result_extract["audit start date"] = sentence[sentence.index(
                            text) + 1]
                    else:
                        result_extract["audit start date"] = None
    return result_extract


def check_major(text, result_extract):
    """Checking the major non conformities value

    Args:
        text (str): the text that has been extracted from the pdf file
        result_extract (Dict[str, str]): the dictionary that contains the result that has been extracted

    Returns:
        result_extract (Dict[str, str]): the dictionary that contains the reuslt that has been extracted
    """
    splitter = text.split("major")
    text = next(s for s in splitter if s).strip()
    if text.isdigit():
        result_extract["major"] = (text, 0)


def get_auditor_info(sentence_list: List,
                     result_extract: Dict[str, str],
                     current_text: str) -> Dict[str, str]:
    """Get the auditor name and company information

    Args:
        sentence_list (List): _description_
        result_extract (List): _description_
        current_text (List): _description_

    Returns:
        result_extract (Dict[str, str]): _description_
    """
    result_extract["auditor company"] = sentence_list[sentence_list.index(
        current_text) - 1]
    result_extract["auditor name"] = current_text.lower().split(
        "auditor: ")[-1]
    return result_extract


def check_audit_result(text: str, result_extract: Dict[str, str]) -> Dict[str, str]:
    """Get the audit result based on the pdf file
    Args:
        text (str): the input text to find info
        result_extract (Dict[str, str]): the current result dictionary

    Returns:
        result_extract (Dict[str, str]): the updated version of result dictionary
    """
    if "audit grade" in text:
        regex_checker(text, AUDIT_RESULT_HEADERS, result_extract)

    return result_extract


def get_address(pdf_file: BytesIO, result_extract: Dict[str, str]) -> Dict[str, str]:
    """Get the address of the company

    Args:
        pdf_file (BytesIO): _description_
        result_extract (Dict[str, str]): the current result dictionary

    Returns:
        result_extract (Dict[str, str]): the updated version of result dictionary
    """
    for page_number in range(1, 5):
        with plumber.open(pdf_file) as file:
            doc = file.pages[page_number]
            word = doc.extract_words()

            non_dup_list = [dict(t) for t in {tuple(d.items()) for d in word}]
            sorted_dictionary = sorted(
                non_dup_list, key=lambda d: (d["top"], d['x0']))
        index_list = []
        for index, value in enumerate(sorted_dictionary):
            if value["text"] == "Address":
                index_list.append(index)
            elif value["text"] == "Country":
                index_list.append(index)
            result_text_list = [i["text"] for i in sorted_dictionary]

            # print(" ".join(resultTextList[range[0] + 1:range[1]]))
            result_extract["address"] = " ".join(
                result_text_list[index_list[0] + 1: index_list[1]])
            return result_extract


def brc_scan(pdf_path: BytesIO, result_extract: Dict[str, str]) -> Dict[str, str]:
    """Main Function for extracting key information from PDF

    Args:
        pdf_file (BytesIO): _description_
        result_extract (Dict[str, str]): the current result dictionary

    Returns:
        result_extract (Dict[str, str]): the updated version of result dictionary
    """
    with plumber.open(pdf_path) as pdf_file:
        for page_number in range(2):
            doc = pdf_file.pages[page_number]
            sentence = doc.extract_text(y_tolerance=5).split(
                "\n")  # extract text and split by line
            sentence = [text.strip()
                        for text in sentence if text]  # strip the word
            # remove blank values
            sentence = [text for text in sentence if text]
            st.write(sentence)

            for text in sentence:
                if "auditor:" in text.lower():
                    get_auditor_info(sentence, result_extract, text)
                elif "major" in text.lower():
                    check_major(text.lower(), result_extract)
                elif "audit result" in text.lower():
                    check_audit_result(text.lower(), result_extract)
                else:
                    regex_checker(text, KEY_HEADERS, result_extract)

    return result_extract
