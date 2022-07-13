"""SQF OCR Module"""
from __future__ import annotations
import io
import itertools

import re
import copy
from typing import Dict, List, Tuple
from contextlib import suppress

import fitz
import easyocr
import streamlit as st
import pdfplumber as plumber


KEY_HEADERS = {
    'food sector categories',
    'products',
    'scope of certification',
    'phone #',
    'email',
    'web site',
    'cb#',
    'accreditation body',
    'accreditation number',
    'lead auditor',
    'technical reviewer',
    'hours spent on site',
    'hours of ict activities',
    'hours spent writing report',
    'hours writing report',
    'hours auditing'
}

HEADER_CONVERTER = (
    'audit decision',
    'decision date',
    'recertification date',
    'expiration date',
    'certification number',
    'audit type',
    'audit dates',
    'issue date',
    'audit rating',
)

BOTTOM_DICT_HEADERS = {
    'food sector categories',
    'products',
    'scope of certification',
    'phone #',
    'email',
    'web site',
    'cb#',
    'accreditation body',
    'accreditation number',
    'lead auditor',
    'technical reviewer',
    'hours spent on site',
    'hours of ict activities',
    'hours spent writing report',
    'hours writing report',
    'hours auditing',
}

BOTTOM_DICT_REGEX_DELIMITER = re.compile(
    '|'.join(BOTTOM_DICT_HEADERS), re.IGNORECASE)
REGEX_NON_CONFORMITIES = re.compile(
    r'(?<=response:)(?:minor|major|fundamental|critical)', re.IGNORECASE)

@st.cache(persist = True)
def init_reader() -> None:
    """Initialize the reader OCR"""
    READER = easyocr.Reader(['en'])

    return READER

def pdf_to_image(file_contents: bytes):
    """Convert PDF Bytes to Image contents

    Args:
        file_contents (bytes): the pdf file contents

    Returns:
        image (PIL.Image): the image bytes
    """
    with fitz.open(stream=file_contents, filetype='pdf') as doc:
        zoom = 2
        matrix = fitz.Matrix(zoom, zoom)
        page = doc.load_page(0)
        first_page_pixmap = page.get_pixmap(matrix=matrix)
        image = first_page_pixmap.tobytes()
        return image

# Run easy-ocr on image


def run_ocr(image) -> List[Tuple[List[str], str]]:
    """Run the OCR through the image to extract text
    Args:
        image: the Image that will use to do OCR

    Returns:
        paragraph_text (List[Tuple[List[str], str]): list of text after OCR the image
    """
    READER = init_reader()

    if not READER:
        return []

    paragraph_text = READER.readtext(image, paragraph=True)
    return paragraph_text


def postprocessing(ocr_result: Dict[str, Tuple[str, int]]) -> Dict[str, Tuple[str, int]]:
    """Cleaning and post processing the result after extract

    Args:
        ocr_result (Dict[str, Tuple[str, int]]): the result after OCR extraction

    Returns:
        Dict[str, Tuple[str, int]]: the result dictionary contains page number and text
    """
    end_result = {}
    regex_subs = (
        re.compile(r"(\(*([0-9]+)[\)|\.]+)"),
        re.compile(
            r"(@\[a-z0-9]+)|([^0-9a-z \t\/\-])|(\w+:\/\S+)|^rt|http.+?", re.IGNORECASE),
    )
    for key, value in ocr_result.items():
        text, page_number = value
        if isinstance(text, str):
            for regex in regex_subs:
                text = regex.sub('', text)
            end_result[key] = (text, page_number)
        else:
            end_result[key] = value
        if key == "audit dates":
            with suppress(ValueError):
                start_date, end_date = text.rsplit(" ", 1)
                end_result["audit start period"] = (start_date, page_number)
                end_result["audit end period"] = (end_date, page_number)
                end_result.pop("audit dates", None)

        return end_result


def fix_audit_rating(paragraph_list: List[Tuple[List[str], str]],
                     result_dictionary: Dict[str, int]):
    """Fixing the audit rating after OCR from the file

    Args:
        paragraph_list (List[Tuple[List[str], str]]): the OCR text list after extract from file
        result_dictionary (Dict[str, int]): the result dictionary

    Returns:
        paragraph_list (List[Tuple[List[str], str]]): the OCR text list after extract from file
        bottom_result (List): the bottom result
    """
    bottom_result_index = None
    rating_key = None
    score_value = None

    for index, (rating, text) in enumerate(paragraph_list):
        if text.lower() == "audit rating":
            rating_key = (rating, text)
        if text.lower() == "facility & scope":
            result_dictionary["facility"] = (
                paragraph_list[index + 2][1].strip(), 0)
        if text.isnumeric():
            score_value = (rating, text)

    if rating_key and score_value:
        item_list = (
            [rating_key[0][0], score_value[0][1],
                rating_key[0][2], score_value[0][3]],
            f"{rating_key[1]} {score_value[1]}",
        )
        paragraph_list.append(item_list)

    bottom_result = copy.copy(paragraph_list[bottom_result_index:])

    return paragraph_list, bottom_result


def create_top_dict(paragraph_list: List[Tuple[List[str], str]],
                    result_dictionary: Dict[str, Tuple[str | int, int]]) -> None:
    """Get the result on top of the page SQF

    Args:
        paragraph_list (List[Tuple[List[str], str]]): the OCR text list after extract from file
        result_dictionary (Dict[str, Tuple[str  |  int, int]]): the result dictionary
    """
    for _, text in paragraph_list:
        with suppress(ValueError):  # Ruling out unnecessary texts
            first, second, value = text.strip().split(' ', 2)
            if (key := f"{first} {second}".lower().strip()) in HEADER_CONVERTER:
                result_dictionary[key] = (value.strip(), 0)


def create_bottom_dict(paragraph_list: List[Tuple[List[str], str]],
                       result_dictionary: Dict[str, Tuple[str | int, int]]) -> None:
    """Get the result on the bottom of the page SQF

    Args:
        paragraph_list (List[Tuple[List[str], str]]): the OCR text list after extract from file
        result_dictionary (Dict[str, Tuple[str  |  int, int]]): the result dictionary
    """
    for _, text in paragraph_list:
        delimiters = BOTTOM_DICT_REGEX_DELIMITER.findall(text)
        values = [text.strip()
                  for text in BOTTOM_DICT_REGEX_DELIMITER.split(text)[1:]]
        for delimiter, value in zip(delimiters, values):
            result_dictionary[delimiter] = (value.strip(), 0)


def count_nonconformities_single_page(page_file):
    """Count the number of non-conformities of each page and extract out"""
    text = page_file.extract_text()
    return REGEX_NON_CONFORMITIES.findall(text)


def count_total_nonconformities(pdf_file: bytes,
                                result_dictionary: Dict[str, Tuple[str | int, int]]):
    """Count the total number of non-conformities that appear in the PDF file

    Args:
        pdf_file (bytes): the pdf file in contents of bytes
        result_dictionary (Dict[str, Tuple[str  |  int, int]]): the result dictionary
    """
    with plumber.open(io.BytesIO(pdf_file)) as pdf:
        for page_number in pdf.pages:
            non_conformities = count_nonconformities_single_page(page_number)

        non_conformities = tuple(x for x in itertools.chain.from_iterable(
            x for x in non_conformities if x) if x)
        non_conformities_dict = {key.lower(): (
            non_conformities.count(key), None) for key in set(non_conformities)}
        result_dictionary.update(non_conformities_dict)


def sqf_scan(file_contents: bytes) -> Dict[str, Tuple[str, int]]:
    first_page_image = pdf_to_image(file_contents)
    paragraph_list = run_ocr(first_page_image)
    results = {}
    paragraph_list, bottom_result = fix_audit_rating(paragraph_list, results)
    create_top_dict(paragraph_list, results)
    create_bottom_dict(bottom_result, results)
    count_total_nonconformities(file_contents, results)
    final = postprocessing(results)

    return final
